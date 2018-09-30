
Using the Session
-----------------
The `orm.mapper()` function and declarative extensions are the primary configurational interface for the ORM. Once mappings are configured, the primary usage interface for persistence operations is the `Session`.

Session establishes all conversations with the database and represents a “holding zone” for all the objects which you’ve loaded or associated with it during its lifespan. It provides the entrypoint to acquire a Query object, which sends queries to the database using the Session object’s current database connection, populating result rows into objects that are then stored in the Session, inside a structure called the Identity Map - a data structure that maintains unique copies of each object, where “unique” means “only one object with a particular primary key”.
All changes to objects maintained by a Session are tracked - before the database is queried again or before the current transaction is committed, it flushes all pending changes to the database. This is known as the Unit of Work pattern.
When using a Session, it’s important to note that the objects which are associated with it are proxy objects to the transaction being held by the Session - there are a variety of events that will cause objects to re-access the database in order to keep synchronized.

**Unit of work**

Maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems.
Solves issues: keep track of what you've changed, to write back into the database. Similarly, objects created/deleted. Keeping track of the objects you've read so you can avoid inconsistent reads
You can change the database with each change to your object model, but this can lead to lots of very small database calls, which ends up being very slow and requires you to have a transaction open for the whole interaction, which can be impractical.
A Unit of Work keeps track of everything you do during a business transaction that can affect the database. When you're done, it figures out everything that needs to be done to alter the database as a result of your work.

**Flushing**

To sync the state of your application data with the state of the data in the database.

What the difference is between `flush()` and `commit()` in SQLAlchemy?

A `Session` object is basically an ongoing transaction of changes to a database (update, insert, delete).
The session object registers transaction operations with `session.add()`, but doesn't yet communicate them to the database until session.flush() is called.

`session.flush()` communicates a series of operations to the database. The database maintains them as pending operations in a transaction. The changes aren't persisted permanently to disk, or visible to other transactions until the database receives a `COMMIT` for the current transaction.

When you use a `Session` object to query the database, the query will return results both from the database and from the flushed parts of the uncommitted transaction it holds. By default, Session objects autoflush their operations, but this can be disabled:

    s = Session()

    s.add(Foo('A')) # The Foo('A') object has been added to the session.
                    # It has not been committed to the database yet,
                    #   but is returned as part of a query.
    print 1, s.query(Foo).all()
    s.commit()

    s2 = Session()
    s2.autoflush = False

    s2.add(Foo('B'))
    print 2, s2.query(Foo).all() # The Foo('B') object is *not* returned
                                 #   as part of this query because it hasn't
                                 #   been flushed yet.
    s2.flush()                   # Now, Foo('B') is in the same state as
                                 #   Foo('A') was above.
    print 3, s2.query(Foo).all()
    s2.rollback()                # Foo('B') has not been committed, and rolling
                                 #   back the session's transaction removes it
                                 #   from the session.
    print 4, s2.query(Foo).all()

    #---
    Output:
    1 [<Foo('A')>]
    2 [<Foo('A')>]
    3 [<Foo('A')>, <Foo('B')>]
    4 [<Foo('A')>]

Specifically, the flush occurs before any individual `Query` is issued, as well as within the `commit()` call before the transaction is committed.

**Commit and Rollback**

Another behavior of `commit()` is that by default it expires the state of all instances present after the commit is complete. This is so that when the instances are next accessed, either through attribute access or by them being present in a Query result set, they receive the most recent state.

When a `flush()` fails, typically for reasons like primary key, foreign key, or “not nullable” constraint violations, a `rollback()` is issued automatically

**Getting a sessions**

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # an Engine, which the Session will use for connection
    some_engine = create_engine('postgresql://scott:tiger@localhost/')

    # create a configured "Session" class.
    # This factory, when called, will create a new Session object using the supplied configurational arguments
    Session = sessionmaker(bind=some_engine)

    # create a Session
    session = Session()

    # work with sess
    myobject = MyObject('foo', 'bar')
    session.add(myobject)
    session.commit()

When you write your application, place the sessionmaker factory at the global level. This factory can then be used by the rest of the application as the source of new Session instances, keeping the configuration for how Session objects are constructed in one place.

*When do I make a sessionmaker?* Just one time, somewhere in your application’s global scope. It should be looked upon as part of your application’s configuration. If your application has three .py files in a package, you could, for example, place the `sessionmaker` line in your `__init__.py` file; from that point on your other modules say “from mypackage import Session”. That way, everyone else just uses `Session()`, and the configuration of that session is controlled by that central point.

*When do I construct a Session, when do I commit it, and when do I close it?*

As a general rule, keep the lifecycle of the session separate and external from functions and objects that access and/or manipulate database data. This will greatly help with achieving a predictable and consistent transactional scope.
Make sure you have a clear notion of where transactions begin and end, and keep transactions **short**, meaning, they end at the series of a sequence of operations, instead of being held open indefinitely.

*Is the session thread-safe*

The bigger point is that you should not want to use the session with multiple concurrent threads. The session is a local “workspace” that you use for a specific set of tasks; don’t share that session with other thread.
Not sharing the Session implies a more significant pattern; it means not just the `Session` object itself, but also **all objects that are associated with that Session**, must be kept within the scope of a single concurrent thread.

**Basics of Using a Session**

    # query from a class
    session.query(User).filter_by(name='ed').all()

    # query with multiple classes, returns tuples
    session.query(User, Address).join('addresses').filter_by(name='ed').all()

    # query using orm-enabled descriptors
    session.query(User.name, User.fullname).all()

    ser1 = User(name='user1')
    session.add(user1)
    session.commit()     # write changes to the database

To add a list of items to the session at once, use add_all():

    session.add_all([item1, item2, item3])

    session.delete(obj1)
    # commit (or flush)
    session.commit()

Deleting Objects Referenced from Collections and Scalar Relationships:

The ORM in general never modifies the contents of a collection or scalar relationship during the flush process. This means, if your class has a relationship() that refers to a collection of objects, or a reference to a single object such as many-to-one, the contents of this attribute will not be modified when the flush process occurs.

This behavior is not to be confused with the flush process’ impact on column- bound attributes that refer to foreign key and primary key columns; these attributes are modified liberally within the flush, since these are the attributes that the flush process intends to manage.

ven though rows related to the deleted object might be themselves modified as well, **no changes occur to relationship-bound collections or object references on the objects** involved in the operation within the scope of the flush itself. This means if the object was a member of a related collection, it will still be present on the Python side until that collection is expired. Similarly, if the object were referenced via many-to-one or one-to-one from another object, that reference will remain present on that object until the object is expired as well:

    >>> address = user.addresses[1]
    >>> session.delete(address)
    >>> session.flush()
    >>> address in user.addresses
    True

    >>> session.commit()
    >>> address in user.addresses
    False

Basic Relationship Patterns
---------------------------

`backref` parameter allows you to declare both relationships with single declaration: it means to automatically install backward relationship in related class. I personally prefer using backref for self-referring relationships only, as I like self-documented code (avoid having to look through other classes, probably defined in other modules) - see `back_populates`

`back_populates` takes a string name and has the same meaning as `backref`, except the complementing property is not created automatically, and instead must be configured explicitly on the other mapper.

**One To Many**

FK on the child table referencing the parent. `relationship()` is then specified on the parent, as referencing a collection of items represented by the child

    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, ForeignKey
    from sqlalchemy.orm import relationship, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    engine = create_engine('sqlite:///:memory:', echo=True)
    Base = declarative_base(bind=engine)

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        # children = relationship("Child")
        children = relationship("Child", back_populates="parent")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)
        parent_id = Column(Integer, ForeignKey('parent.id'))
        # parent = relationship("Parent")
        parent = relationship("Parent", back_populates="children")

    parent = Parent(id=1)
    child = Child(id=5)
    child.parent = parent
    print([a.id for a in parent.children])
    #[5] n.b. if use relationship without back_populates you get []

**Many To One**

Many to one places a foreign key in the parent table referencing the child. `relationship()` is declared on the parent, where a new scalar-holding attribute will be created

Bidirectional behavior is achieved by adding a second `relationship(` and applying the `relationship.back_populates` parameter in both directions:
Alternatively, the backref parameter may be applied to a single `relationship()`, such as Parent.child:

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Parent(Base):
        __tablename__ = 'parent'
        id = Column(Integer, primary_key=True)
        child_id = Column(Integer, ForeignKey('child.id'))
        child = relationship("Child", backref="parents")

    class Child(Base):
        __tablename__ = 'child'
        id = Column(Integer, primary_key=True)

**One to One**

A bidirectional relationship with a scalar attribute on both sides. To achieve this, the `uselist` flag indicates the placement of a scalar attribute instead of a collection on the “many” side of the relationship:

**Many to Many**

Adds an association table between two classes. The association table is indicated by the secondary argument to `relationship()`
Usually, the Table uses the MetaData object associated with the declarative base class, so that the ForeignKey directives can locate the remote tables with which to link:

For a bidirectional relationship, both sides of the relationship contain a collection. Specify using relationship.back_populates, and for each `relationship()` specify the common association table:

    association_table = Table('association', Base.metadata,
        Column('left_id', Integer, ForeignKey('left.id')),
        Column('right_id', Integer, ForeignKey('right.id'))
    )

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship(
            "Child",
            secondary=association_table,
            back_populates="parents")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)
        parents = relationship(
            "Parent",
            secondary=association_table,
            back_populates="children")

When using the `backref` parameter instead of `relationship.back_populates`, the backref will automatically use the same secondary argument for the reverse relationship:

The secondary argument of `relationship()` also accepts a callable that returns the ultimate argument, which is evaluated only when mappers are first used, i.e. after all module initialization is complete:

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Child",
                        secondary=lambda: association_table,
                        backref="parents")

**Association object**

In the association object pattern, the many-to-many table is mapped by a full class instead of using the secondary argument to `relationship()`. It’s used when your association table contains additional columns beyond those which are foreign keys to the left and right tables.

he bidirectional version makes use of `relationship.back_populates` or `relationship.backref`:

    class Association(Base):
        __tablename__ = 'association'
        left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
        right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
        extra_data = Column(String(50))
        child = relationship("Child", back_populates="parents")
        parent = relationship("Parent", back_populates="children")

    class Parent(Base):
        __tablename__ = 'left'
        id = Column(Integer, primary_key=True)
        children = relationship("Association", back_populates="parent")

    class Child(Base):
        __tablename__ = 'right'
        id = Column(Integer, primary_key=True)
        parents = relationship("Association", back_populates="child")

Working with the association pattern in its direct form requires that child objects are associated with an association instance before being appended to the parent; similarly, access from parent to child goes through the association object:

    # create parent, append a child via association
    p = Parent()
    a = Association(extra_data="some data")
    a.child = Child()
    p.children.append(a)

    # iterate through child objects via association, including association
    # attributes
    for assoc in p.children:
        print(assoc.extra_data)
        print(assoc.child)

Mapper Configuration
--------------------

In “classical” form, the table metadata is created separately with the Table construct, then associated with the User class via the mapper() function:

    from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
    from sqlalchemy.orm import mapper

    metadata = MetaData()

    user = Table('user', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(50)),
                Column('fullname', String(50)),
                Column('password', String(12))
            )

    class User(object):
        def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password

    mapper(User, user)

The Declarative Mapping is the typical way that mappings are constructed in modern SQLAlchemy. Making use of the Declarative system, the components of the user-defined class as well as the Table metadata to which the class is mapped are defined at once:

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, ForeignKey

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)

        addresses = relationship("Address", backref="user", order_by="Address.id")

    class Address(Base):
        __tablename__ = 'address'

        id = Column(Integer, primary_key=True)
        user_id = Column(ForeignKey('user.id'))
        email_address = Column(String)

Additional attributes, such as relationships to other mapped classes, are also declared inline within the class definition.

**Declarative API**

Provides a syntactical shortcut to the cls argument sent to `declarative_base()`, allowing the base class to be converted in-place to a “declarative” base:

    @as_declarative()
    class Base(object):
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()
        id = Column(Integer, primary_key=True)

    class Parent(Base):
        # children = relationship("Child")
        children = relationship("Child", back_populates="parent")

    class Child(Base):
        parent_id = Column(Integer, ForeignKey('parent.id'))
        # parent = relationship("Parent")
        parent = relationship("Parent", back_populates="children")

`@declared_attr` is usually applicable to mixins; turns the attribute into a scalar-like property that can be invoked from the uninstantiated class.

    class ProvidesUser(object):

        @declared_attr
        def user(self):
            return relationship("User")

**Runtime Inspection API system**

Using the `inspect()` function, one can acquire the `Mapper` from a mapped class:

    >>> from sqlalchemy import inspect
    >>> insp = inspect(Child)
    >>> print(list(insp.columns))
    [Column('id', Integer(), table=<child>, primary_key=True, nullable=False), Column('parent_id', Integer(), ForeignKey('parent.id'), table=<child>)]

Mixin and Custom Base Classes
-----------------------------
For sharing functionality (common columns, table options, mapped properties etc.) across many classes when using `declarative`,
i.e. custom declarative base class and “mixins”.

    class MyMixin(object):

        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

        __table_args__ = {'mysql_engine': 'InnoDB'}
        __mapper_args__= {'always_refresh': True}

        id =  Column(Integer, primary_key=True)

    class MyModel(MyMixin, Base):
        name = Column(String(100))

Normal Python method resolution rules apply. The above example would work the same if `Base` preceded `MyMixin`
because `Base` here doesn’t define any of the variables that `MyMixin` defines. If the `Base` did define an attribute of the same name, the class placed first in the inherits list would determine which attribute is used.

**Augmenting the Base**

In addition to using a pure mixin, most of the techniques in this section can also be applied to the base class itself, for patterns that should apply to all classes derived from a particular base:

    from sqlalchemy.ext.declarative import declared_attr

    class Base(object):
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

        __table_args__ = {'mysql_engine': 'InnoDB'}

        id =  Column(Integer, primary_key=True)

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base(cls=Base)

    class MyModel(Base):
        name = Column(String(1000))

**Mixing in Columns**

The most basic way to specify a column on a mixin is by simple declaration:

    class TimestampMixin(object):
        created_at = Column(DateTime, default=func.now())

    class MyModel(TimestampMixin, Base):
        __tablename__ = 'test'

        id =  Column(Integer, primary_key=True)
        name = Column(String(1000))

For columns that have foreign keys, and various mapper-level constructs that require destination-explicit context, the declared_attr decorator is used:

    class ReferenceAddressMixin(object):
        @declared_attr
        def address_id(cls):
            return Column(Integer, ForeignKey('address.id'))

    class User(ReferenceAddressMixin, Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)

**Mixing in Relationship**

Below is an example which combines a foreign key column and a relationship so that two classes Foo and Bar can both be configured to reference a common target class via many-to-one:

    class RefTargetMixin(object):
        @declared_attr
        def target_id(cls):
            return Column('target_id', ForeignKey('target.id'))

        @declared_attr
        def target(cls):
            return relationship("Target")

    class Foo(RefTargetMixin, Base):
        __tablename__ = 'foo'
        id = Column(Integer, primary_key=True)

    class Bar(RefTargetMixin, Base):
        __tablename__ = 'bar'
        id = Column(Integer, primary_key=True)

    class Target(Base):
        __tablename__ = 'target'
        id = Column(Integer, primary_key=True)

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




