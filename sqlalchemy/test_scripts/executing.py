from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
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

ins = users.insert().values(name='jack', fullname='Jack Jones')
result = conn.execute(ins)

ins2 = users.insert().values(name='jacky', fullname='Jack Smith')
result2 = conn.execute(ins)

print(result2.inserted_primary_key)

s = select([users])
result3 = conn.execute(s)
print(type(result3))

print(users.c.id == 7)
print((users.c.id == 7).compile().params)

conn.execute(addresses.insert(), [
   {'user_id': 1, 'email_address': 'jack@yahoo.com'},
   {'user_id': 1, 'email_address': 'jack@msn.com'},
   {'user_id': 2, 'email_address': 'www@www.org'},
   {'user_id': 2, 'email_address': 'wendy@aol.com'},
])

stmt = stmt.columns(users.c.id, users.c.name)