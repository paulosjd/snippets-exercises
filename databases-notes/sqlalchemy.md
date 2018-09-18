    dialect+driver://username:password@host:port/database

    e = create_engine("mysql://scott:tiger@localhost/test")

To connect to PostgreSQL database, need psycopg2,the Python drivers for PostgreSQL

    from sqlalchemy import create_engine
    engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')

You could also connect to your database using the psycopg2 driver exclusively:

    import psycopg2
    conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
    conn = psycopg2.connect(conn_string)

However, using the psycopg2 driver to connect does not take advantage of SQLAlchemy, which allows you to think in terms of Python objects rather than database semantics, and that there is an obvious place to perform validation and checking of incoming data.

**Raw DBAPI connection**

    from sqlalchemy import text

    sql = text('select name from penguins')
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])
    print(names)


    from sqlalchemy.sql import text

    connection = engine.connect()

    # recommended
    cmd = 'select * from Employees where EmployeeGroup == :group'
    employeeGroup = 'Staff'
    employees = connection.execute(text(cmd), group = employeeGroup)


