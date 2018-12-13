import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr, as_declarative
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

class ColorSet(enum.Enum):
    one = 'red'
    two = 'green'
    three = 'blue'

class Department(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(Enum(ColorSet))

class Employee(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(Department, backref=backref('employees', uselist=True))

engine = create_engine('sqlite:///')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

john = Employee(name='john')
dan = Employee(name='dan')
it_department = Department(name='IT', color=ColorSet.two)
john.department = it_department
dan.department = it_department

s = session()

s.add(john)
s.add(dan)
s.add(it_department)
s.commit()

it = s.query(Department).filter(Department.name == 'IT').one()
print(it.employees[0].name)
# john

find_it = select([Employee.name]).where(Department.name == 'IT')
find_it2 = select([Employee.name]).where(Department.id == john.department_id)
print(s.execute(find_it2).fetchall())
# ('john', )