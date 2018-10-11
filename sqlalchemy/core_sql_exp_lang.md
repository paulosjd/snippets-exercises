SQL Expression Language
-----------------------
A system of representing relational database structures and expressions using Python constructs.
While the constructs attempt to represent equivalent concepts between backends with consistent structures, they do not conceal useful concepts that are unique to particular subsets of backends. The Expression Language therefore presents a method of writing backend-neutral SQL expressions, but does not attempt to enforce that expressions are backend-neutral.

The Expression Language is in contrast to the Object Relational Mapper, which is a distinct API that builds on top of the Expression Language.
Whereas the ORM presents a high level and abstracted pattern of usage, the Expression Language presents a system of representing the primitive constructs of the relational database directly without opinion.

One approaches the structure and content of data from the perspective of a user-defined domain model which is transparently persisted and refreshed from its underlying storage model. The other approaches it from the perspective of literal schema and SQL expression representations which are explicitly composed into messages consumed individually by the database.

**Connecting**

For this tutorial we will use an in-memory-only SQLite database. This is an easy way to test things without needing to have an actual database defined anywhere. To connect we use `create_engine()`:

    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('sqlite:///:memory:', echo=True)

The `echo` flag is a shortcut to setting up SQLAlchemy logging, setting to `True` allows us to see the SQL produced.

The return value of `create_engine()` is an instance of Engine, and it represents the core interface to the database, adapted through a dialect that handles the details of the database and DBAPI in use. In this case the SQLite dialect will interpret instructions to the Python built-in sqlite3 module.
Lazy Connecting - the `Engine`, when first returned by `create_engine()`, has not actually tried to connect to the database yet. The first time a method like `Engine.execute()` or `Engine.connect()` is called, the `Engine` establishes a real DBAPI connection to the database, which is then used to emit the SQL.

**Define and Create Tables**

See above sections relating to `MetaData` and `MetaData.create_all()`

    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    >>> metadata = MetaData()
    >>> users = Table('users', metadata,
    ...     Column('id', Integer, primary_key=True),
    ...     Column('name', String),
    ...     Column('fullname', String),
    ... )

    >>> addresses = Table('addresses', metadata,
    ...   Column('id', Integer, primary_key=True),
    ...   Column('user_id', None, ForeignKey('users.id')),
    ...   Column('email_address', String, nullable=False)
    ...  )

**Insert Expressions and Executings**

    >>> ins = users.insert()
    >>> str(ins)
    'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'

The engine object we created is a repository for database connections capable of issuing SQL to the database. To acquire a connection, we use the `connect()` method:

    >>> conn = engine.connect()

The Connection object represents an actively checked out DBAPI connection resource. Lets feed it our Insert object:

    >>> ins = users.insert().values(name='jack', fullname='Jack Jones')
    >>> result = conn.execute(ins)
    INSERT INTO users (name, fullname) VALUES (?, ?)
    ('jack', 'Jack Jones')
    COMMIT

As the SQLAlchemy Connection object references a DBAPI connection, the result, known as a `ResultProxy object`, is analogous to the DBAPI cursor object.

    >>> result.inserted_primary_key
    [1]

Create a generic insert statement and then use it the 'normal way':

    >>> ins = users.insert()
    >>> conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')

To issue many inserts using DBAPI’s `executemany()` method, we can send in a list of dictionaries. Note each dictionary must have the same set of keys.

    >>> conn.execute(addresses.insert(), [
    ...    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
    ...    {'user_id': 2, 'email_address' : 'www@www.org'},
    ...    {'user_id': 2, 'email_address' : 'wendy@aol.com'},
    ... ])
    INSERT INTO addresses (user_id, email_address) VALUES (?, ?)
    ((1, 'jack@yahoo.com'), (1, 'jack@msn.com'), (2, 'www@www.org'), (2, 'wendy@aol.com'))
    COMMIT
    <sqlalchemy.engine.result.ResultProxy object at 0x...>

**PEP 249 DB-API**

"...call the cursor's `fetchone()` method to retrieve a single matching row, or call `fetchall()` to ..."
Notice that these methods are available on `ResultProxy` objects

**Selecting**

    >>> from sqlalchemy.sql import select
    >>> s = select([users])
    >>> result = conn.execute(s)

    >>> for row in result:
    ...     print(row)
    (1, u'jack', u'Jack Jones')
    (2, u'wendy', u'Wendy Williams')

    >>> result = conn.execute(s)
    >>> row = result.fetchone()
    # print("name:", row[1], "; fullname:", row[2])
    >>> print("name:", row['name'], "; fullname:", row['fullname'])
    name: jack ; fullname: Jack Jones

To specify columns which are placed in the COLUMNS clause of the select, we reference individual `Column` objects from our `Table`. These are available as named attributes off the `c` attribute of the `Table` object.
It can be useful to use the `Column` objects directly as keys:

    >>> for row in conn.execute(s):
    ...     print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])
    name: jack ; fullname: Jack Jones
    name: wendy ; fullname: Wendy Williams

Result sets which have pending rows remaining should be explicitly closed before discarding:

    >>> result.close()

Put two tables into `select()` statement, with help of a `WHERE` clause using `Select.where()`:

    >>> s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
    sql
    >>> for row in conn.execute(s):
    ...     print(row)
    (1, u'jack', u'Jack Jones', 1, 1, u'jack@yahoo.com')
    (1, u'jack', u'Jack Jones', 2, 1, u'jack@msn.com')
    (2, u'wendy', u'Wendy Williams', 3, 2, u'www@www.org')
    (2, u'wendy', u'Wendy Williams', 4, 2, u'wendy@aol.com')

Note that with just simple Python equality operator the argument would just be `True`, not a clause. If you call `str()` on it you see it produces SQL:

    >>> users.c.id == addresses.c.user_id
    <sqlalchemy.sql.elements.BinaryExpression object at 0x...>
    >>> str(users.c.id == addresses.c.user_id)
    'users.id = addresses.user_id'

**Operators**

Here we get a bind parameter (a placeholder like `?` or `:name`):

    >>> print(users.c.id == 7)
    users.id = :id_1

    >>> (users.c.id == 7).compile().params
    {u'id_1': 7}

Most Python operators produce a SQL expression here:

    >>> print(users.c.id != 7)
    users.id != :id_1

    >>> # None converts to IS NULL
    >>> print(users.c.name == None)
    users.name IS NULL

Adding two interger columns gives an addition expresssion:

    >>> print(users.c.id + addresses.c.id)
    users.id + addresses.id

Adding two string columns gives concatenation:

    >>> print(users.c.name + users.c.fullname)
    users.name || users.fullname

Where `||` is the concatenation operator on most databases.

SQL that’s generated for an Engine that’s connected to a MySQL database; the `||` operator now compiles as MySQL’s `concat()` function

**Conjunctions**

Conjunctions are those little words like AND and OR that put things together. We’ll also hit upon NOT and LIKE:

`and_()`, `or_()`, `not_()`, `between()` correspond to the SQL operators.  `label()` is used in a column expression to produce labels using the `AS` keyword

We can build up a `select()` construct through successive method calls (method-chaining):

    >>> s = select([(users.c.fullname +
    ...               ", " + addresses.c.email_address).
    ...                label('title')]).\
    ...        where(
    ...           and_(
    ...               users.c.id == addresses.c.user_id,
    ...               users.c.name.between('m', 'z'),
    ...               or_(
    ...                  addresses.c.email_address.like('%@aol.com'),
    ...                  addresses.c.email_address.like('%@msn.com')
    ...               )
    ...           )
    ...        )

A shortcut to using `and_()` is to chain together multiple `where()` clauses. The above can also be written as:

    >>> s = select([(users.c.fullname +
    ...               ", " + addresses.c.email_address).
    ...                label('title')]).\
    ...        where(users.c.id == addresses.c.user_id).\
    ...        where(users.c.name.between('m', 'z')).\
    ...        where(
    ...               or_(
    ...                  addresses.c.email_address.like('%@aol.com'),
    ...                  addresses.c.email_address.like('%@msn.com')
    ...               )
    ...        )
    >>> conn.execute(s).fetchall()
    SELECT users.fullname || ? || addresses.email_address AS title
    FROM users, addresses
    WHERE users.id = addresses.user_id AND users.name BETWEEN ? AND ? AND
    (addresses.email_address LIKE ? OR addresses.email_address LIKE ?)
    (', ', 'm', 'z', '%@aol.com', '%@msn.com')
    [(u'Wendy Williams, wendy@aol.com',)]

**Text in SQL Expression Language**

Going from what one understands to be a textual SQL expression into a Python construct which groups components together in a programmatic style can be hard.

The `text()` construct is used to compose a textual statement that is passed to the database mostly unchanged. Below, we create a `text()` object and execute it:

    >>> from sqlalchemy.sql import text
    >>> s = text(
    ...     "SELECT users.fullname || ', ' || addresses.email_address AS title "
    ...         "FROM users, addresses "
    ...         "WHERE users.id = addresses.user_id "
    ...         "AND users.name BETWEEN :x AND :y "
    ...         "AND (addresses.email_address LIKE :e1 "
    ...             "OR addresses.email_address LIKE :e2)")
    sql
    >>> conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()
    [(u'Wendy Williams, wendy@aol.com',)]

`text()` fragments within bigger statements

The `select()` object accepts `text()` objects as an argument for most of its builder functions. In so, the `select()` construct provides the “geometry” of the statement, and the `text()` construct provides the textual content within this form. We can build a statement without the need to refer to any pre-established `Table` metadata:

    >>> s = select([
    ...        text("users.fullname || ', ' || addresses.email_address AS title")
    ...     ]).\
    ...         where(
    ...             and_(
    ...                 text("users.id = addresses.user_id"),
    ...                 text("users.name BETWEEN 'm' AND 'z'"),
    ...                 text(
    ...                     "(addresses.email_address LIKE :x "
    ...                     "OR addresses.email_address LIKE :y)")
    ...             )
    ...         ).select_from(text('users, addresses'))
    sql
    >>> conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()
    [(u'Wendy Williams, wendy@aol.com',)]

Specifying Bound Parameter Behaviors:

    stmt = text("SELECT * FROM users WHERE users.name BETWEEN :x AND :y")
    stmt = stmt.bindparams(x="m", y="z")

    >>> from sqlalchemy.sql import bindparam
    >>> s = users.select(users.c.name == bindparam('username'))
    >>> conn.execute(s, username='wendy').fetchall()
    [(2, u'wendy', u'Wendy Williams')]

    >>> s = users.select(users.c.name.like(bindparam('username', type_=String) + text("'%'")))
    >>> conn.execute(s, username='wendy').fetchall()
    [(2, u'wendy', u'Wendy Williams')]

**`TextClause.columns()`**

Specify the return types, based on name:

    stmt = stmt.columns(id=Integer, name=String)

Or it can be passed full column expressions positionally:

    stmt = text("SELECT id, name FROM users")
    stmt = stmt.columns(users.c.id, users.c.name)

    >>> stmt = text("SELECT users.id, addresses.id, users.id, "
    ...     "users.name, addresses.email_address AS email "
    ...     "FROM users JOIN addresses ON users.id=addresses.user_id "
    ...     "WHERE users.id = 1").columns(
    ...        users.c.id,
    ...        addresses.c.id,
    ...        addresses.c.user_id,
    ...        users.c.name,
    ...        addresses.c.email_address
    ...     )
    sql
    >>> result = conn.execute(stmt)

The `TextClause.columns()` method is typically very applicable to textual statements to be used in an ORM context.

**Using More Specific Text with table(), literal_column(), and column()**

By using `column()`, `literal_column()`, and `table()` for some of the key elements of our statement. Using these constructs, we can get some more expression capabilities than if we used `text()` directly, as they provide to the Core more information about how the strings they store are to be used, but still without the need to get into full `Table` based metadata.

    s = select([
       literal_column("users.fullname", String) +
       ', ' +
       literal_column("addresses.email_address").label("title")]
    ).select_from(table('users')).select_from(table('addresses'))

Notice that by using `literal_column()`, we did not need to refer to users or addresses metadata

**Ordering or Grouping by a Label**

when our statement has some labeled column element that we want to refer to in a place such as the “ORDER BY” or “GROUP BY” clause; other candidates include fields within an “OVER” or “DISTINCT” clause. If we have such a label in our `select()` construct, we can refer to it directly by passing the string straight into `select.order_by()` or `select.group_by()`, among others.

    >>> from sqlalchemy import func
    >>> stmt = select([
    ...         addresses.c.user_id,
    ...         func.count(addresses.c.id).label('num_addresses')]).\
    ...         order_by("num_addresses")
    >>> conn.execute(stmt).fetchall()
    [(2, 4)]

**Using Aliases**

The alias in SQL corresponds to a “renamed” version of a table or SELECT statement, which occurs anytime you say “SELECT .. FROM sometable AS someothername”. The AS creates a new name for the table. Aliases are a key construct as they allow any table or subquery to be referenced by a unique name. In the case of a table, this allows the same table to be named in the FROM clause multiple times. In the case of a SELECT statement, it provides a parent name for the columns represented by the statement, allowing them to be referenced relative to this name.

In SQLAlchemy, any `Table`, `select()` construct, or other selectable can be turned into an alias using the `FromClause.alias()` method, which produces a `Alias` construct.

E.g., How can we locate jack based on the combination of two addresses we know he has? To accomplish this, we’d use a join to the addresses table, once for each address. We create two Alias constructs against addresses, and then use them both within a `select()` construct:

    >>> a1 = addresses.alias()
    >>> a2 = addresses.alias()
    >>> s = select([users]).\
    ...        where(and_(
    ...            users.c.id == a1.c.user_id,
    ...            users.c.id == a2.c.user_id,
    ...            a1.c.email_address == 'jack@msn.com',
    ...            a2.c.email_address == 'jack@yahoo.com'
    ...        ))
    >>> conn.execute(s).fetchall()
    [(1, u'jack', u'Jack Jones')]

**Using Joins**

We’ve already been doing joins in our examples, by just placing two tables in either the columns clause or the where clause of the `select()` construct. E.g.:

    s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
    result = conn.execute(s)

    # gives same output as the above
    s2 = select([users, addresses]).select_from(users.join(addresses))
    result2 = conn.execute(s2)

If we want to make a real “JOIN” or “OUTERJOIN” construct, we use the `join()` and `outerjoin()` methods, most commonly accessed from the left table in the join:

    >>> print(users.join(addresses))
    users JOIN addresses ON users.id = addresses.user_id

Notice how SQLAlchemy figured out how to JOIN the two tables. The ON condition of the join was automatically generated based on the `ForeignKey` object

To join on a certain expression, e.g.  join on all users who use the same name in their email address as their username:

    >>> print(users.join(addresses,
    ...                 addresses.c.email_address.like(users.c.name + '%')
    ...             )
    ...  )
    users JOIN addresses ON addresses.email_address LIKE users.name || :name_1

With a `select()` construct, SQLAlchemy looks around at the tables we’ve mentioned and then places them in the FROM clause of the statement. When we use JOINs however, we know what FROM clause we want, so here we make use of the `select_from()` method:

    >>> s = select([users.c.fullname]).select_from(
    ...    users.join(addresses,
    ...             addresses.c.email_address.like(users.c.name + '%'))
    ...    )
    >>> conn.execute(s).fetchall()
    [(u'Jack Jones',), (u'Jack Jones',), (u'Wendy Williams',)]

**SQL Functions**

    >>> from sqlalchemy.sql import func
    >>> print(func.concat('x', 'y'))
    concat(:concat_1, :concat_2)

Creates an SQL function based on chosen word. Functions are most typically used in the columns clause of a select statement, and can also be labeled as well as given a type. Labeling a function is recommended so that the result can be targeted in a result row based on a string name, and assigning it a type is required when you need result-set processing to occur, such as for Unicode conversion and date conversions. Below, we use the result function scalar() to just read the first column of the first row and then close the result; the label, even though present, is not important in this case:

    >>> conn.execute(
    ...     select([
    ...            func.max(addresses.c.email_address, type_=String).
    ...                label('maxemail')
    ...           ])
    ...     ).scalar()
    u'www@www.org'

    # using min() gives 'jack@msn.com'

**Correlated subqueries**

SQLAlchemy automatically correlates embedded FROM objects to that of an enclosing query.
Auto-correlation will usually do what’s expected, however it can also be controlled. For example, if we wanted a statement to correlate only to the addresses table but not the users table, even if both were present in the enclosing SELECT, we could do so using the `correlate()` method to specify those FROM clauses that may be correlated.

To entirely disable a statement from correlating, we can pass `None` as the argument:

    >>> stmt = select([users.c.id]).\
    ...             where(users.c.name == 'wendy').\
    ...             correlate(None)
    >>> enclosing_stmt = select([users.c.name]).\
    ...     where(users.c.id == stmt)
    >>> conn.execute(enclosing_stmt).fetchall()
    SELECT users.name
     FROM users
     WHERE users.id = (SELECT users.id
      FROM users
      WHERE users.name = ?)
    ('wendy',)
    [(u'wendy',)]

**Ordering, Grouping, Limiting, Offset…ing…**

Chain on e.g. `.order_by(users.c.name.desc())`

Grouping refers to the GROUP BY clause, and is usually used in conjunction with aggregate functions to establish groups of rows to be aggregated:

    stmt = select([users.c.name, func.count(addresses.c.id)]). \
            select_from(users.join(addresses)). \
            group_by(users.c.name)

HAVING can be used to filter results on an aggregate value, after GROUP BY has been applied:

>>> stmt = select([users.c.name, func.count(addresses.c.id)]).\
...             select_from(users.join(addresses)).\
...             group_by(users.c.name).\
...             having(func.length(users.c.name) > 4)
>>> conn.execute(stmt).fetchall()

A common system of dealing with duplicates in composed SELECT statements is the DISTINCT modifier:

    >>> stmt = select([users.c.name]).\
    ...             where(addresses.c.email_address.
    ...                    contains(users.c.name)).\
    ...             distinct()
    >>> conn.execute(stmt).fetchall()
    SELECT DISTINCT users.name
    FROM users, addresses
    WHERE (addresses.email_address LIKE '%' || users.name || '%')
    ()
    [(u'jack',), (u'wendy',)]


