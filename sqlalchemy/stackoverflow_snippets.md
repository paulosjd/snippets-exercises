IN clause
---------
I'm trying to do this query in sqlalchemy:

    SELECT id, name FROM user WHERE id IN (123, 456)

session.query(MyUserClass).filter(MyUserClass.id.in_((123,456))).all()

Subqueries
-----------

    SELECT *
    FROM Residents
    WHERE apartment_id IN (SELECT ID
                           FROM Apartments
                           WHERE postcode = 2000)

Use the [subquery](http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html#sqlalchemy.orm.query.Query.subquery) method:

    subquery = session.query(Apartments.id).filter(Apartments.postcode==2000).subquery()
    query = session.query(Residents).filter(Residents.apartment_id.in_(subquery))

------------------------
    class User(db.Model):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True)

    class Posts(db.Model):
        __tablename__ = 'posts'
        post_id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
        post_time = db.Column(db.DateTime)

        user = db.relationship('User', backref='posts')

How would I go about querying for a list of users and their newest post (excluding users with no posts). If I was using SQL, I would do:

    SELECT [whatever]
    FROM posts AS p
        LEFT JOIN users AS u ON u.user_id = p.user_id
    WHERE p.post_time = (SELECT MAX(post_time) FROM posts WHERE user_id = u.user_id)

This should work (different SQL, same result):

    t = Session.query(
        Posts.user_id,
        func.max(Posts.post_time).label('max_post_time'),
    ).group_by(Posts.user_id).subquery('t')

    query = Session.query(User, Posts).filter(and_(
        User.user_id == Posts.user_id,
        User.user_id == t.c.user_id,
        Posts.post_time == t.c.max_post_time,
    ))

    for user, post in query:
        print user.user_id, post.post_id
----------


