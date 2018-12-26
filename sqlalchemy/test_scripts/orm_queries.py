from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, func, and_
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr, as_declarative

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

class Exchange(Base):
    name = Column(String)
    country = Column(String)

class Shares(Base):
    company = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    exchange = relationship(Exchange, backref=backref('shares'))

engine = create_engine('sqlite:///')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

s = session()

nyse = Exchange(name='NYSE', country='USA')
nasdaq = Exchange(name='NASDAQ', country='Canada')

s.add(nyse)
s.add(nasdaq)

goog1 = Shares(company='Google', price=95, quantity=5, exchange=nyse)
goog2 = Shares(company='Google', price=95, quantity=20, exchange=nyse)
goog3 = Shares(company='Google', price=104, quantity=15, exchange=nyse)
goog3 = Shares(company='Google', price=104, quantity=25, exchange=nyse)
goog3 = Shares(company='Google', price=92, quantity=30, exchange=nyse)
msoft = Shares(company='Microsoft', price=84, quantity=40, exchange=nasdaq)

for i in [goog1, goog2, goog3, msoft]:
    s.add(i)

s.commit()

# select price, sum(quantity) as num from shares where company='Google' group by price;

prices = s.query(Shares.price, func.sum(Shares.quantity)) \
                .filter(Shares.company == 'Google').group_by(Shares.price).all()
print(prices)

prices = s.query(Shares.price, func.sum(Shares.quantity).label('total_sold')) \
                .filter(Shares.company == 'Google').group_by(Shares.price).first()
print(prices.total_sold)

us_shares = s.query(Shares.company)\
    .join(Exchange, Exchange.id == Shares.id)\
    .filter(Exchange.country == 'USA').all()

print(us_shares)

number = s.query(func.sum(Shares.quantity).label('number')).as_scalar()

prices = s.query(Shares.price, Shares.quantity)\
            .join(Exchange, Exchange.id == Shares.exchange_id)\
            .filter(and_(
                Exchange.name == 'NYSE',
                number > 20)
            ).group_by(Shares).all()
print(prices)





