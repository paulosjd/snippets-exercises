Relationship Loading Techniques
-------------------------------

**The N+1 problem in relational databases**

A common side effect of the lazy load pattern. Suppose you have a user table and each user has bought a number of products, listed in a sales table. To get a list of all products bought by users in the last 2 days, this could be done by:

    SELECT * FROM User;

and then for each user, you query the number of products they have bought:

    SELECT * FROM Sales WHERE user_id = ? AND date > two_days_ago

In other words, you have one Select statement for the user table followed by N additional Select statements to get the associated products, where N is the total number of users.

Each access to the database has a certain overhead, this will scale quite badly with the number of users.
If you would write pure SQL, you would directly see the number of select statements you submit, while in SQLAlchemy it is not obvious so it is important to understand the loading options.

    #Flask-SQLAlchemy
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ...
        products = db.relationship('product',
                                   secondary=sales)

We have two main choices for how we can implement the products relationship defined above. The default setting of SQLAlchemy is lazy loading, which means that the related rows in the sales table are not loaded together with the user object.
In this case lazy loading means we will run into the N+1 problem.

To solve this problem we have to make use of the lazy keyword, which by default is set to 'select' like this

    products = db.relationship('product', secondary=sales, lazy='select')

One useful option is `lazy='dynamic'` like this

    products = db.relationship('product',
                               secondary=sales,
                               lazy='dynamic')

Here, `user.products` returns a query object rather than table rows. This gives you a lot of flexibility how the second database access might look. E.g. you could add additional filters:

    user.products.filter_by(Products.date > two_days_ago).all()

This can be very useful, say if there are many rows in the products table, the additional filter might make the second database access much quicker.
However, it will still need a second trip to the database. To avoid the N+1 problem we need to load the rows in the sales table together with the users.

To do this we have to make use of eager loading and SQLAlchemy provides three choices for that: joined loading `(lazy='joined')`, subquery loading `(lazy='subquery')` and select IN loading `(lazy='selectin')`

Let's start with the subquery loading since that one is often a good choice. Here two Select statements are run, one to retrieve all users and one to retrieve all related rows in the sales table. So rather N+1 we have 2 Select statements.

Alternatively, joined loading squeezes everything into one Select statement. So we save another Select statement compared to subquery loading, but the downside is that if the products table is large, this can become very slow since it makes use of an outer left join.

More commonly, instead of adding this loading option to the mapping, the loading style is set at runtime. You can do that with `joinedload()`, `subqueryload()`, `selectinload()` and `lazyload()`:

    from sqlalchemy.orm import subqueryload, joinedload, selectinload

    users = User.query.options(selectinload(User.products)).all()

**Controlling Loading via Options**

Configure loading strategies on a per-query basis against specific attributes.

The most common loader options are `joinedload()`, `subqueryload()`, `selectinload()` and `lazyload()`

    # set children to load lazily
    session.query(Parent).options(lazyload('children')).all()

    # same, using class-bound attribute
    session.query(Parent).options(lazyload(Parent.children)).all()

    # set children to load eagerly with a join
    session.query(Parent).options(joinedload('children')).all()

The loader options can also be “chained” using method chaining to specify how loading should occur further levels deep:

    session.query(Parent).options(
        joinedload(Parent.children).
        subqueryload(Child.subelements)).all()

Chained loader options can be applied against a “lazy” loaded collection. This means that when a collection or association is lazily loaded upon access, the specified option will then take effect:

    session.query(Parent).options(
        lazyload(Parent.children).
        subqueryload(Child.subelements)).all()

Navigate along a path without changing the existing loader style of a particular attribute:

    session.query(A).options(
        defaultload("atob").
        joinedload("btoc")).all()

**Lazy Loading**

Default for inter-object relationships is known as “lazy” or “select” loading - the name “select” because a “SELECT” statement is typically emitted when the attribute is first accessed.

The scalar or collection attribute associated with a `relationship()` contains a trigger which fires the first time the attribute is accessed. This trigger typically issues a SQL call at the point of access:

    >>> jack.addresses
    SELECT
        addresses.id AS addresses_id,
        addresses.email_address AS addresses_email_address,
        addresses.user_id AS addresses_user_id
    FROM addresses
    WHERE ? = addresses.user_id
    [5]
    [<Address(u'jack@google.com')>, <Address(u'j25@yahoo.com')>]

While lazy loading can be expensive for related collections, in the case that one is loading lots of objects with simple many-to-ones against a relatively small set of possible target objects, lazy loading may be able to refer to these objects locally without emitting as many SELECT statements as there are parent objects.

**Addressing the N+1 problem with `raiseload()**

 The problem of code that may access other attributes that were not eagerly loaded, where lazy loading is not desired, may be addressed using the raiseload() strategy; this loader strategy replaces the behavior of lazy loading with an informative error being raised.

    from sqlalchemy.orm import raiseload
    session.query(User).options(raiseload(User.addresses))

Above, a `User` object loaded from the above query will not have the `.addresses` collection loaded; if some code later on attempts to access this attribute, an ORM exception is raised.

To set up only one attribute as eager loading, and all the rest as raise (by using a wildcard specifier):

    session.query(Order).options(
    joinedload(Order.items), raiseload('*'))

**Joined Eager Loading**

Connects a JOIN (by default a LEFT OUTER join) to the SELECT statement emitted by a Query and populates the target scalar/collection from the same result set as that of the parent.

Usually used for collections rather than many-to-one-references.

    >>> jack = session.query(User).\
    ... options(joinedload(User.addresses)).\
    ... filter_by(name='jack').all()
    SELECT
        addresses_1.id AS addresses_1_id,
        addresses_1.email_address AS addresses_1_email_address,
        addresses_1.user_id AS addresses_1_user_id,
        users.id AS users_id, users.name AS users_name,
        users.fullname AS users_fullname,
        users.password AS users_password
    FROM users
    LEFT OUTER JOIN addresses AS addresses_1
        ON users.id = addresses_1.user_id
    WHERE users.name = ?
    ['jack']

The JOIN emitted by default is a LEFT OUTER JOIN, to allow for a lead object that does not refer to a related row. For an attribute that is guaranteed to have an element, such as a many-to-one reference to a related object where the referencing foreign key is NOT NULL, the query can be made more efficient by using an inner join:

    session.query(Address).options(
    joinedload(Address.user, innerjoin=True))

**The Zen of Joined Eager Loading**

It is critical to understand the distinction that while `Query.join()` is used to alter the results of a query, `joinedload()` goes through great lengths to not alter the results of the query, and instead hide the effects of the rendered join to only allow for related objects to be present.

The philosophy behind loader strategies is that any set of loading schemes can be applied to a particular query, and the results don’t change - only the number of SQL statements required to fully load related objects and collections changes. A particular query might start out using all lazy loads. After using it in context, it might be revealed that particular attributes or collections are always accessed, and that it would be more efficient to change the loader strategy for these. The strategy can be changed with no other modifications to the query, the results will remain identical, but fewer SQL statements would be emitted. In theory (and pretty much in practice), nothing you can do to the Query would make it load a different set of primary or related objects based on a change in loader strategy.

**Subquery Eager Loading and Select IN loading**

Is configured in the same manner as that of joined eager loading.  Using `subqueryload()` option rather than `joinedload()` option can give greater query than joined eager loading in the area of loading collections.

Select IN loading is similar but has a much simpler structure than that of subquery eager loading, and is often superior.
This style of loading emits a SELECT that refers to the primary key values of the parent object inside of an IN clause, in order to load related associations:

    >>> jack = session.query(User).\
    ... options(selectinload('addresses')).\
    ... filter(or_(User.name == 'jack', User.name == 'ed')).all()
    SELECT
        users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.password AS users_password
    FROM users
    WHERE users.name = ? OR users.name = ?
    ('jack', 'ed')
    SELECT
        users_1.id AS users_1_id,
        addresses.id AS addresses_id,
        addresses.email_address AS addresses_email_address,
        addresses.user_id AS addresses_user_id
    FROM users AS users_1
    JOIN addresses ON users_1.id = addresses.user_id
    WHERE users_1.id IN (?, ?)
    ORDER BY users_1.id, addresses.id
    (5, 7)

Above, the second SELECT refers to `users_1.id IN (5, 7)`, where the “5” and “7” are the primary key values for the previous two User objects loaded; after a batch of objects are completely loaded, their primary key values are injected into the IN clause for the second SELECT.

**What Kind of Loading to Use ?**

Typically comes down to optimizing the tradeoff between number of SQL executions, complexity of SQL emitted, and amount of data fetched. Lets take two examples, a relationship() which references a collection, and a `relationship()` that references a scalar many-to-one reference.

One to Many Collection

default lazy loading: if you load 100 objects, and then access a collection on each of them, a total of 101 SQL statements will be required.

joined loading: the same would only one emit SQL statement. However, the total number of rows fetched will be equal to the sum of the size of all the collections, plus one extra row for each parent object that has an empty collection. Each row will also contain the full set of columns represented by the parents, repeated for each collection item. Therefore joined eager loading only makes sense when the size of the collections are relatively small.

subquery loading: makes sense when the collections are larger.

selectin loading: the load of 100 objects will also emit two SQL statements, the second of which refers to the 100 primary keys of the objects loaded

Many to One Reference

default lazy loading: if the many-to-one reference is a simple foreign key reference to the target’s primary key, each reference will be checked first in the current identity map using `Query.get()`. So here, if the collection of objects references a relatively small set of target objects, using the default of `lazy=’select’` is by far the most efficient way to go.

joined loading: For a load of objects where there are many possible target references which may have not been loaded already, joined loading with an INNER JOIN is extremely efficient. Configure with `innerjoin=True` if FK reference is not nullable.

not much advantage for subquery loading or selectin loading
