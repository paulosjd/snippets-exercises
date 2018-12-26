from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(engine)
Base = declarative_base(engine)

session = Session()


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('region.id'), index=True)

    parent = relationship(lambda: Region, remote_side=id, backref='sub_regions')


Base.metadata.create_all()

r1 = Region(name='United States of America')
r2 = Region(name='California', parent=r1)
r2 = Region(name='Ohio')


session.add_all((r1, r2))
session.commit()

region_alias = aliased(Region)

usa = session.query(Region).join(region_alias, region_alias.id == Region.id).all()
print([a.name for a in usa])
usa = session.query(region_alias).join(Region, Region.id == region_alias.id).all()
print([a.name for a in usa])


#
# adam = Person(id=1, name='Adam', age=33)
# eve = Person(id=2, name='Eve', age=32)
#
# s.add(adam)
# s.add(eve)
#
# cain = Person(id=3, name='Cain', age=21, parent=adam)
# abel = Person(id=4, name='Eve', age=17, parent=eve)
#
# s.add(cain)
# s.add(abel)
#
#
# s.commit()

# select price, sum(quantity) as num from shares where company='Google' group by price;

# query = s.query(Person.name)\
#             .join(Person)\
#             .all()
# print(query)
#
#




