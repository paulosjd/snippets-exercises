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
