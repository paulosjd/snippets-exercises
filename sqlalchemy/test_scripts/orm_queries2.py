import datetime
from sqlalchemy import Column, String, Date, Integer, ForeignKey, create_engine, func, and_, or_
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr, as_declarative

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

class Country(Base):
    name = Column(String)
    currency_symbol = Column(String)

class Exchange(Base):
    name = Column(String)
    date_opened = Column(Date)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='exchanges')

class Company(Base):
    name = Column(String)
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    exchange = relationship('Exchange', backref='companies')

class Shares(Base):
    price = Column(Integer)
    quantity = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship('Company', backref='shares')

engine = create_engine('sqlite:///')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

s = session()

usa = Country(name='USA', currency_symbol='$')
canada = Country(name='Canada', currency_symbol='C$')
aus = Country(name='Australia', currency_symbol='A$')
s.add(usa)
s.add(canada)
s.add(aus)

nyse = Exchange(name='NYSE', date_opened=datetime.date(1996, 10, 10), country=usa)
nasdaq = Exchange(name='NASDAQ', date_opened=datetime.date(1986, 8, 12), country=canada)
asx = Exchange(name='ASX', date_opened=datetime.date(1997, 8, 12), country=aus)

s.add(nyse)
s.add(nasdaq)
s.add(asx)

google = Company(name='Google', exchange=nyse)
microsoft = Company(name='Microsoft', exchange=nasdaq)
csl = Company(name='CSL', exchange=asx)

s.add(google)
s.add(microsoft)
s.add(csl)

goog1 = Shares(company=google, price=95, quantity=5)
goog2 = Shares(company=google, price=95, quantity=20)
goog3 = Shares(company=google, price=104, quantity=15)
goog4 = Shares(company=google, price=104, quantity=25)
goog5 = Shares(company=google, price=92, quantity=30)
csl1 = Shares(company=csl, price=82, quantity=20)
csl2 = Shares(company=csl, price=86, quantity=10)
msoft = Shares(company=microsoft, price=84, quantity=40)
msoft2 = Shares(company=microsoft, price=84, quantity=40)


for i in [goog1, goog2, goog3, goog4, goog5, csl1, csl2, msoft, msoft2]:
    s.add(i)
s.commit()

sub_query2 = s.query(Exchange.id).join(Country, Country.id == Exchange.country_id)\
                .filter(Exchange.date_opened > datetime.date(1996, 12, 12)).all()

query = s.query(Shares.price, Company.name, Exchange.name)\
            .join(Company, Company.id == Shares.company_id)\

query = query.join(Exchange, Exchange.id == Company.exchange_id)\
            .filter(Exchange.id.in_([a.id for a in sub_query2]))\
            .all()

print(query)

sub_query2 = s.query(Exchange.id).join(Country, Country.id == Exchange.country_id)\
                .filter(Exchange.date_opened > datetime.date(1996, 12, 12)).subquery()

query = s.query(Shares.price, Company.name, Exchange.name)\
            .join(Company, Company.id == Shares.company_id)\
            .join(Exchange, Exchange.id == Company.exchange_id)\
            .filter(Exchange.id.in_(sub_query2))\
            .all()

print(query)

