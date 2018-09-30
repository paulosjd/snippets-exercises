from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(bind=engine)


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'))
    children = relationship("Child", backref="parents")


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)

Base.metadata.create_all()

# parent = Parent()

# session.add(parent)
# session.commit()

# child = Child(parent_id=parent.id)

# session.add(child)
# session.commit()
#
# print("children: {}".format(parent.children[0].id))
# print("parent: {}".format(child.parent.id))

parent = Parent(id=1)
child = Child(id=5)
child.parents.append(parent)

print([a.id for a in child.parents])
