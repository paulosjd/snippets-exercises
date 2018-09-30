Part 1 - SQL Expression Language
--------------------------------
The follow assume this as a starting point:

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

Names where fullname contains 'Jack J'

    conn.execute(select([users.c.name]).where(users.c.fullname.like('Jack J%'))).fetchall()

Users which have last name beginning with 'J':

    conn.execute(select([users]).where(users.c.fullname.like(users.c.name + ' ' + 'J%'))).fetchall()

    conn.execute(select([users]).where(users.c.fullname.contains(' J'))).fetchall()

Show set of users who have their names in their email addresses. [Solution](https://docs.sqlalchemy.org/en/latest/core/tutorial.html#using-joins)

    conn.execute(select([users.c.name, addresses.c.email_address])
                   .select_from(users.join(addresses, addresses.c.email_address.like(users.c.name + '%')))).fetchall()

The same with WHERE clause instead of JOIN:

    conn.execute(select([users]).where(addresses.c.email_address.contains(users.c.name)).distinct()).fetchall()

Show counts of email addresses for each user. [Solution](https://docs.sqlalchemy.org/en/latest/core/tutorial.html#ordering-grouping-limiting-offset-ing)

    stmt = select([users.c.name, func.count(addresses.c.email_address)]). \
             select_from(users.join(addresses)).group_by(users.c.name)

The same, but for users with more than 1 email address:

    stmt.having(func.count(addresses.c.email_address) > 1)
