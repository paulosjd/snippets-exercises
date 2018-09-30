from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@as_declarative(bind=engine)
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

# Base.metadata.bind = engine  -so can remove bind=engine kwarg to @as_declarative

class Parent(Base):
    # children = relationship("Child")
    children = relationship("Child", back_populates="parent")

class Child(Base):
    parent_id = Column(Integer, ForeignKey('parent.id'))
    # parent = relationship("Parent")
    parent = relationship("Parent", back_populates="children")

Base.metadata.create_all()


parent = Parent(id=1)
child = Child(id=5)
child2 = Child(id=7)

child.parent = parent
parent.children.append(child2)

print([a.id for a in parent.children])
print(child.parent.id)

print(Parent.__tablename__)

# @declared_attr turns the attribute into a scalar-like property that can be invoked from the uninstantiated class.
# Declarative treats attributes specifically marked with @declared_attr as returning a construct that is specific to
# mapping or declarative table configuration. The name of the attribute is that of what the non-dynamic version of the
# attribute would be.


print(Base.metadata.sorted_tables)

engine.connect()
engine.connect()
