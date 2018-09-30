from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, text
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
conn.execute(ins)

ins2 = users.insert().values(name='jacky', fullname='Jack Smith')
conn.execute(ins)

conn.execute(addresses.insert(), [
   {'user_id': 1, 'email_address': 'jack@yahoo.com'},
   {'user_id': 1, 'email_address': 'jack@msn.com'},
   {'user_id': 2, 'email_address': 'www@www.org'},
   {'user_id': 2, 'email_address': 'wendy@aol.com'},
])

stmt = text("SELECT * FROM users WHERE users.name BETWEEN :x AND :y")
stmt = stmt.bindparams(x="d", y="k")
print([row for row in conn.execute(stmt)])

print(select([users.c.id]).where(users.c.name > 1))

s = select([users, addresses]).where(users.c.id == addresses.c.user_id)

result = conn.execute(s)
print([row for row in result.fetchall()])