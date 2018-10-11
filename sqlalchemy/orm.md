
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

**Runtime Inspection API system**

Using the `inspect()` function, one can acquire the `Mapper` from a mapped class:

    >>> from sqlalchemy import inspect
    >>> insp = inspect(Child)
    >>> print(list(insp.columns))
    [Column('id', Integer(), table=<child>, primary_key=True, nullable=False), Column('parent_id', Integer(), ForeignKey('parent.id'), table=<child>)]

Mixin and Custom Base Classes
-----------------------------
[Docs](https://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html)
For sharing functionality (common columns, table options, mapped properties etc.) across classes when using `declarative`,
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

Loading Columns
---------------
Additional options regarding the loading of columns

**Deferred Column Loading**

This feature allows particular columns of a table be loaded only upon direct access, instead of when the entity is queried using Query. This feature is useful when one wants to avoid loading a large text or binary field into memory when it’s not needed. Individual columns can be lazy loaded by themselves or placed into groups that lazy-load together, using the `orm.deferred()` function when defining a mapping:

    from sqlalchemy.orm import deferred
    from sqlalchemy import Integer, String, Text, Binary, Column

    class Book(Base):
        ...
        book_id = Column(Integer, primary_key=True)
        excerpt = deferred(Column(Text))
        photo = deferred(Column(Binary))

Deferred columns can be associated with a “group” name, so that they load together when any of them are first accessed.
You can defer or undefer columns at the Query level using options, including `orm.defer()` and `orm.undefer()`:

    session.query(MyClass).options(
                        defer("attribute_one"),
                        defer("attribute_two"))

    session.query(MyClass).options(
                        defer(MyClass.attribute_one),
                        defer(MyClass.attribute_two))

    # undefer two columns
    session.query(MyClass).options(undefer("col1"), undefer("col2"))

    # undefer all columns specific to a single class using Load + *
    session.query(MyClass, MyOtherClass).options(
        Load(MyClass).undefer("*"))

**Load Only Cols**

Indicate that for a particular entity, only the given list of column-based attribute names should be loaded; all others will be deferred.

This function is part of the `Load` interface and supports both method-chained and standalone operation.

Example - given a class `User`, load only the name and fullname attributes:

    session.query(User).options(load_only("name", "fullname"))

Example - given a relationship `User.addresses -> Address`, specify subquery loading for the `User.addresses` collection, but on each `Address` object load only the `email_address` attribute:

    session.query(User).options(
            subqueryload("addresses").load_only("email_address")
    )

For a `Query` that has multiple entities, the lead entity can be specifically referred to using the `Load` constructor:

    session.query(User, Address).join(User.addresses).options(
                Load(User).load_only("name", "fullname"),
                Load(Address).load_only("email_addres")
            )

SQL Expressions as Mapped Attributes
------------------------------------
Attributes on a mapped class can be linked to SQL expressions, which can be used in queries.

**Hybrid property**

The easiest and most flexible way to link relatively simple SQL expressions to a class; provides for an expression that works at both the Python level as well as at the SQL expression level.

    from sqlalchemy.ext.hybrid import hybrid_property

    class User(Base):
        ...
        firstname = Column(String(50))
        lastname = Column(String(50))

        @hybrid_property
        def fullname(self):
            return self.firstname + " " + self.lastname

Above, the `fullname` attribute is interpreted at both the instance and class level, so that it is available from an instance:

    some_user = session.query(User).first()
    print(some_user.fullname)

as well as usable within queries:

    some_user = session.query(User).filter(User.fullname == "John Smith").first()

Cascades
--------
Refer to how operations performed on a “parent” object relative to a particular `Session` should be propagated to items referred to by that relationship

The default value of `cascade` is `save-update, merge`. The typical alternative setting for this parameter is either all or more commonly all, delete-orphan. The all symbol is a synonym for save-update, merge, refresh-expire, expunge, delete, and using it in conjunction with delete-orphan indicates that the child object should follow along with its parent in all cases, and be deleted once it is no longer associated with that parent.

Cascade behavior is configured using the `cascade` option on `relationship()`:

    class Order(Base):
        __tablename__ = 'order'

        items = relationship("Item", cascade="all, delete-orphan")
        customer = relationship("User", cascade="save-update")

To set cascades on a `backref`, the same flag can be used with the `backref()` function:

    class Item(Base):
        __tablename__ = 'item'

        order = relationship("Order",
                        backref=backref("items", cascade="all, delete-orphan")
                    )

The `save-update` cascade is on by default, and is typically taken for granted; it simplifies code by allowing a single call to `Session.add()` to register an entire structure of objects within that `Session` at once.

    >>> sess.add(user1
    >>> address3 = Address()
    >>> user1.append(address3)
    >>> address3 in sess
    >>> True

[Controlling Cascade on Backrefs](https://docs.sqlalchemy.org/en/latest/orm/cascades.html#controlling-cascade-on-backrefs)
One case where save-update cascade does sometimes get in the way is with bi-directional relationships

    mapper(Order, order_table, properties={
        'items' : relationship(Item, backref='order')
    })

    >>> o1 = Order()
    >>> session.add(o1)
    >>> o1 in session
    True

    >>> i1 = Item()
    >>> i1.order = o1
    >>> i1 in o1.items
    True
    >>> i1 in session
    True

This behavior can be disabled using the cascade_backrefs flag:

    mapper(Order, order_table, properties={
        'items' : relationship(Item, backref='order',
                                    cascade_backrefs=False)
    })

So above, the assignment of `i1.order = o1` will append `i1` to the items collection of `o1`, but will not add `i1` to the session. You can, of course, `add()` `i1` to the session at a later point. This option may be helpful for situations where an object needs to be kept out of a session until it’s construction is completed, but still needs to be given associations to objects which are already persistent in the target session.

**delete**

    class User(Base):
        # ...

        addresses = relationship("Address", cascade="save-update, merge, delete")

If using the above mapping, we have a User object and two related Address objects:

    >>> user1 = sess.query(User).filter_by(id=1).first()
    >>> address1, address2 = user1.addresses

If we mark user1 for deletion, after the flush operation proceeds, address1 and address2 will also be deleted:

    >>> sess.delete(user1)
    >>> sess.commit()
    DELETE FROM address WHERE address.id = ?
    ((1,), (2,))
    DELETE FROM user WHERE user.id = ?
    (1,)
    COMMIT

Alternatively, if our User.addresses relationship does not have delete cascade, SQLAlchemy’s default behavior is to instead de-associate address1 and address2 from user1 by setting their foreign key reference to NULL. Using a mapping as follows:

    class User(Base):
        # ...

        addresses = relationship("Address")

Upon deletion of a parent User object, the rows in address are not deleted, but are instead de-associated:

    >>> sess.delete(user1)
    >>> sess.commit()
    UPDATE address SET user_id=? WHERE address.id = ?
    (None, 1)
    UPDATE address SET user_id=? WHERE address.id = ?
    (None, 2)
    DELETE FROM user WHERE user.id = ?
    (1,)
    COMMIT

delete cascade is more often than not used in conjunction with `delete-orphan` cascade, which will emit a `DELETE` for the related row if the “child” object is deassociated from the parent. The combination of delete and delete-orphan cascade covers both situations where SQLAlchemy has to decide between setting a foreign key column to NULL versus deleting the row entirely.

**ORM-level “delete” cascade vs. FOREIGN KEY level “ON DELETE” cascade**

The behavior of SQLAlchemy’s “delete” cascade has a lot of overlap with the `ON DELETE CASCADE` feature of a database foreign key, as well as with that of the ON `DELETE SET NULL` foreign key setting when “delete” cascade is not specified.

It is important to note the differences between the ORM and the relational database’s notion of “cascade” as well as how they integrate:

A database level `ON DELETE` cascade is configured effectively on the many-to-one side of the relationship; that is, we configure it relative to the FOREIGN KEY constraint that is the “many” side of a relationship. At the ORM level, this direction is reversed. SQLAlchemy handles the deletion of “child” objects relative to a “parent” from the “parent” side, which means that delete and delete-orphan cascade are configured on the one-to-many side.

Database level foreign keys with no `ON DELETE` setting are often used to prevent a parent row from being removed, as it would necessarily leave an unhandled related row present. If this behavior is desired in a one-to-many relationship, SQLAlchemy’s default behavior of setting a foreign key to `NULL` can be caught in one of two ways:

The easiest and most common is just to set the foreign-key-holding column to `NOT NULL` at the database schema level. An attempt by SQLAlchemy to set the column to `NULL` will fail with a simple `NOT NULL` constraint exception.
