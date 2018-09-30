from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, text, func
from sqlalchemy.sql import select


engine = create_engine('sqlite:///:memory:', echo=False)

metadata = MetaData(bind=engine)

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

addresses = Table('addresses', metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', None, ForeignKey('users.id')),
  Column('email_address', String, nullable=False)
)

metadata.create_all(engine)

conn = engine.connect()

conn.execute(users.insert(), [
    {'id': 1, 'name': 'jack', 'fullname': 'Jack Jones'},
    {'id': 2, 'name': 'wendy', 'fullname': 'Wendy Wesley'},
    {'id': 3, 'name': 'james', 'fullname': 'John Jones'},
])

conn.execute(addresses.insert(), [
   {'user_id': 1, 'email_address': 'jack@yahoo.com'},
   {'user_id': 1, 'email_address': 'jack@msn.com'},
   {'user_id': 2, 'email_address': 'www@www.org'},
   {'user_id': 2, 'email_address': 'wendy@aol.com'},
   {'user_id': 3, 'email_address': 'james@aol.com'},
])

s = select([users, addresses]).where(users.c.id == addresses.c.user_id)

result = conn.execute(s)
print(result.fetchall())

s2 = select([users, addresses]).select_from(users.join(addresses))
result2 = conn.execute(s2)
print(result2.fetchall())

s3 = select([users, addresses]).select_from(
    users.join(addresses, addresses.c.email_address.like(users.c.name + '%')))

result3 = conn.execute(s3)
print(result3.fetchall())

scalar_result = conn.execute(
    select([
           func.min(addresses.c.email_address, type_=String).
               label('maxemail')
          ])
    ).scalar()

scalar_result2 = conn.execute(
    select([
           func.max(addresses.c.email_address, type_=String).
               label('maxemail')
          ])
    ).scalar()

print(scalar_result)
print(scalar_result2)

print(conn.execute(select([func.count(addresses.c.email_address)])).fetchall())

stmt = select([users.c.name, func.count(addresses.c.id)]). \
    select_from(users.join(addresses)). \
    group_by(users.c.name)

print(conn.execute(stmt).fetchall())


stmt2 = select([users.c.name, func.count(addresses.c.id)]).\
           select_from(users.join(addresses))
print(conn.execute(stmt2).fetchall())

