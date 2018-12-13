`aliased`
---------
Suppose for example we wanted to join to Address twice. We use `aliased()` to create a distinct alias of Address, and joi

    a_alias = aliased(Address)

    q = session.query(User).\
            join(User.addresses).\
            join(a_alias, User.addresses).\
            filter(Address.email_address=='ed@foo.com').\
            filter(a_alias.email_address=='ed@bar.com')

    Where above, the generated SQL would be similar to:

    SELECT user.* FROM user
        JOIN address ON user.id = address.user_id
        JOIN address AS address_1 ON user.id=address_1.user_id
        WHERE address.email_address = :email_address_1
        AND address_1.email_address = :email_address_2

