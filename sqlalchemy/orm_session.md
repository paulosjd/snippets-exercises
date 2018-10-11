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

State Management
----------------
States an instance can have within a session:

Transient - an instance that’s not in a session, and is not saved to the database; i.e. it has no database identity. The only relationship such an object has to the ORM is that its class has a `mapper()` associated with it.

Pending - when you `add()` a transient instance, it becomes pending. It still wasn’t actually flushed to the database yet, but it will be when the next flush occurs.

Persistent - An instance which is present in the session and has a record in the database. You get persistent instances by either flushing so that the pending instances become persistent, or by querying the database for existing instances (or moving persistent instances from other sessions into your local session).

Deleted - An instance which has been deleted within a flush, but the transaction has not yet completed. Objects in this state are essentially in the opposite of “pending” state; when the session’s transaction is committed, the object will move to the detached state. Alternatively, when the session’s transaction is rolled back, a deleted object moves back to the persistent state.

Detached - an instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session.

The actual state of any mapped object can be viewed at any time using the `inspect()` system:

    >>> from sqlalchemy import inspect
    >>> insp = inspect(my_object)
    >>> insp.persistent
    True

**Refreshing / Expiring**

When we talk about expiration of data we are usually talking about an object that is in the persistent state. For example, if we load an object as follows:

    user = session.query(User).filter_by(name='user1').first()

The above User object is persistent, and has a series of attributes present; if we were to look inside its `__dict__`, we’d see that state loaded:

    >>> user.__dict__
    {
      'id': 1, 'name': u'user1',
      '_sa_instance_state': <...>,
    }

Now the state is removed:

    >>> session.expire(user)
    >>> user.__dict__
    {'_sa_instance_state': <...>}

We see that while the internal “state” still hangs around, the values which correspond to the id and name columns are gone. If we were to access one of these columns and are watching SQL

    >>> print(user.name)

we would see that the ORM initiated a lazy load to retrieve the most recent state from the database. Afterwards, the __dict__ is again populated:

    >>> user.__dict__
    {
      'id': 1, 'name': u'user1',
      '_sa_instance_state': <...>,
    }

The `refresh()` method has a similar interface, but instead of expiring, it emits an immediate SELECT for the object’s row immediately:

    # reload all attributes on obj1
    session.refresh(obj1)

**When to refresh/reload**

Of course, most databases are capable of handling multiple transactions at once, even involving the same rows of data. When a relational database handles multiple transactions involving the same tables or rows, this is when the isolation aspect of the database comes into play. The isolation behavior of different databases varies considerably and even on a single database can be configured to behave in different ways (via the so-called isolation level setting). In that sense, the `Session` can’t fully predict when the same SELECT statement, emitted a second time, will definitely return the data we already have, or will return new data. So as a best guess, it assumes that within the scope of a transaction, unless it is known that a SQL expression has been emitted to modify a particular row, there’s no need to refresh a row unless explicitly told to do so.

The `Session` uses the expiration feature automatically whenever the transaction referred to by the session ends. Whenever `Session.commit()` or `Session.rollback()` is called, all objects within the `Session` are expired,

The `Session.expire()` and `Session.refresh()` methods are used in those cases when one wants to force an object to re-load its data from the database, in those cases when it is known that the current state of data is possibly stale. Reasons for this might include:

Some SQL has been emitted within the transaction outside of the scope of the ORM’s object handling, such as if a Table.update() construct were emitted using the Session.execute() method;

If the application is attempting to acquire data that is known to have been modified in a concurrent transaction, and it is also known that the isolation rules in effect allow this data to be visible.

Managing Transactions
---------------------
A newly constructed `Session` may be said to be in the “begin” state. In this state, the Session has not established any connection or transactional state with any of the `Engine` objects.

The `Session` then receives requests to operate upon a database connection, typically to execute SQL statements via `Session.query()`, `Session.execute()`, or within a flush operation of pending data, which occurs when such state exists and `Session.commit()` or `Session.flush()` is called.

For each `Engine` encountered, a `Connection` is associated with it and when the first `Engine` is operated upon, the `Session` can be said to have left the “begin” state and entered “transactional” state.

For each `Connection`, the `Session` also maintains a `Transaction` object, which is acquired by calling `Connection.begin()`

When the transactional state is completed after a rollback or commit, the Session releases all `Transaction` and `Connection` resources, and goes back to the “begin” state, which will again invoke new Connection and Transaction objects as new requests to emit SQL statements are received.

The example below illustrates this lifecycle:

    engine = create_engine("...")
    Session = sessionmaker(bind=engine)

    # new session.   no connections are in use.
    session = Session()
    try:
        # first query. a Connection is acquired from the Engine,
        # and a Transaction started.
        item1 = session.query(Item).get(1)

        # second query.  the same Connection/Transaction used.
        item2 = session.query(Item).get(2)

        # pending changes are created.
        item1.foo = 'bar'
        item2.bar = 'foo'

        # pending changes above are flushed via flush(),
        # the Transaction is committed, the Connection object closed
        # and discarded, the underlying DBAPI connection
        # returned to the connection pool.
        session.commit()
    except:
        # on rollback, same closure of state as with commit proceeds.
        session.rollback()
        raise
    finally:
        # close the Session. Not usually essential.
        # However, if the commit() or rollback() itself experienced
        # an unanticipated internal failure (e.g. a mis-behaved
        # user-defined event handler), .close() will ensure that
        # invalid state is removed.
        session.close()

**Setting Transaction Isolation Levels**

[Docs.](https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#setting-transaction-isolation-levels)
Isolation (ACID model) refers to the behavior of the transaction at the database level in relation to other transactions occurring concurrently.

When using the ORM `Session`, it acts as a facade for engines and connections, but does not expose transaction isolation directly. For this, we need to act upon the `Engine` or `Connection` as appropriate.

Setting Isolation Engine-Wide:

    eng = create_engine(
        "postgresql://scott:tiger@localhost/test",
        isolation_level='REPEATABLE_READ')

    maker = sessionmaker(bind=eng)
    session = maker()

Setting Isolation for Individual Sessions:

    session = maker(
        bind=engine.execution_options(isolation_level='SERIALIZABLE'))

Setting Isolation for Individual Transactions:

    sess = Session(bind=engine)
        sess.connection(execution_options={'isolation_level': 'SERIALIZABLE'})

    # n.b. isolation level cannot be safely modified on a Connection
    # where a transaction has already started. after commit
    # the connection is released and reverted to previous isolation level.
    sess.commit()
