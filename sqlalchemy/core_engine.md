**Engine Configuration**

SQLAlchemy does not contain its own db drivers, but relies on the DBAPI specification to interact with databases.

![](../images/sqlalchemy_engine.png)

sqlalchemy_engine

    dialect+driver://username:password@host:port/database

    e = create_engine("mysql://scott:tiger@localhost/test")

The MySQL dialect uses mysql-python as the default DBAPI. There are many MySQL DBAPIs available, e.g.:

    engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')

The PostgreSQL dialect uses psycopg2 as the default DBAPI

    from sqlalchemy import create_engine
    # default
    engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
    # psycopg2
    engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

You could also connect to your database using the psycopg2 driver exclusively:

    import psycopg2
    conn_string = "host='localhost' dbname='my_database' user='postgres' password='secret'"
    conn = psycopg2.connect(conn_string)

However, using the psycopg2 driver to connect does not take advantage of SQLAlchemy, which allows you to think in terms of Python objects rather than database semantics, and that there is an obvious place to perform validation and checking of incoming data.

**Raw SQL using DBAPI connection**

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

**Describing Databases with MetaData
------------------------------------

`MetaData` is a container object that keeps together many different features of a database (or multiple databases) being described.

To represent a table, use the `Table` class. Its two primary arguments are the table name, then the `MetaData` object which it will be associated with. The remaining positional arguments are mostly `Column` objects describing each column:

    from sqlalchemy import Table, MetaData

    metadata = MetaData()

    user = Table('user', metadata,
        Column('user_id', Integer, primary_key=True),
        Column('user_name', String(16), nullable=False),
        Column('email_address', String(60)),
        Column('password', String(20), nullable=False)
    )

The MetaData object contains all of the schema constructs we’ve associated with it. For example:

    >>> for t in metadata.sorted_tables:
    ...    print(t.name)
    user
    user_preference
    invoice
    invoice_item

Once a Table has been defined, it has a full set of accessors which allow inspection of its properties. Given the following Table definition:

    employees = Table('employees', metadata,
        Column('employee_id', Integer, primary_key=True),
        Column('employee_name', String(60), nullable=False),
        Column('employee_dept', Integer, ForeignKey("departments.department_id"))
    )

    >>> employees.c.employee_dept.type
    INTEGER
    >>> employees.c.employee_name.nullable
    False
    >>> employees.c.employee_name.key = 'foobar'
    # key defaults to it's name but can be any user-defined string
    >>> employees.c.employee_name.key
    foobar
    >>> employees.c.employee_dept.foreign_keys
    {ForeignKey('departments.department_id')}
    >>> list(employees.c.employee_dept.foreign_keys)
    [ForeignKey('departments.department_id')]
    # get the table related by a foreign key
    >>> list(employees.c.employee_dept.foreign_keys)[0].column.table
    departments

**Creating and Dropping DB Tables and Migrations**

The usual way to issue `CREATE` is to use `create_all()` on the `MetaData` object. This method will issue queries that first check for the existence of each individual table, and if not found will issue the `CREATE` statements:

    engine = create_engine('sqlite:///:memory:')

    metadata.create_all(engine)

`create_all()` creates foreign key constraints between tables usually inline with the table definition itself, and for this reason it also generates the tables in order of their dependency.
`drop_all()` does the exact opposite; the same in the reverse order.

Creating and dropping individual tables can be done via the `create()` and `drop()` methods of `Table`.

    employees = Table('employees', meta,
        ...
    )
    employees.create(engine)

    employees.drop(engine)

To enable the “check first for the table existing” logic, add the `checkfirst=True` argument to `create()` or `drop()`:

    employees.create(engine, checkfirst=True)
    employees.drop(engine, checkfirst=False)

While it’s easy enough to emit `ALTER` statements and similar by hand, such as by passing a string to `Connection.execute()` or by using the DDL construct, database schemas in relation to application code are commonly maintained using schema migration tools - Alembic or SQLAlchemy-Migrate.

