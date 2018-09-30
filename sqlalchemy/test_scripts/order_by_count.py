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
    {'user_id': 3, 'email_address': 'jj24@aol.com'},
])

s = select([users, addresses]).where(users.c.id == addresses.c.user_id)

result = conn.execute(s)
print([row for row in result.fetchall()])

from sqlalchemy import func, literal_column, table

stmt = select([
        addresses.c.user_id,
        func.count(addresses.c.id).label('num_addresses')]).\
        order_by("num_addresses")

conn = engine.connect()

print(conn.execute(stmt).fetchall())

s = select([
   literal_column("users.fullname", String) +
   ', ' +
   literal_column("addresses.email_address").label("title")
]).select_from(table('users')).select_from(table('addresses'))

print(conn.execute(s).fetchall())

stmt = select([addresses.join(users)])

print(conn.execute(stmt).fetchall())


from sqlalchemy.sql import bindparam
s = users.select(users.c.name == bindparam('username'))




stmt = select([users.c.name, func.count(addresses.c.email_address)])\
    .select_from(users.join(addresses)).group_by(users.c.name)



print(conn.execute(stmt.having(func.count(addresses.c.email_address) > 1)).fetchall())

#
# jstmt = select([users.c.name, addresses.c.email_address]).\
#     select_from(users.join(addresses, ad))