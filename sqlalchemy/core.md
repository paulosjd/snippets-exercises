Column and Data Types
---------------------

SQLAlchemy provides abstractions for most common database data types, and a mechanism for specifying your own custom data types.

The methods and attributes of type objects are rarely used directly; they are supplied to Table definitions

    >>> users = Table('users', metadata,
    ...               Column('id', Integer, primary_key=True)
    ...               Column('login', String(32))
    ...              )

SQLAlchemy will use the `Integer` and `String(32)` type information when issuing a CREATE TABLE statement and will use it again when reading back rows SELECTed from the database.

Types include:

`class sqlalchemy.types.BigInteger` is type for bigger `int` integers.
Typically generates a `BIGINT` in DDL, and otherwise acts like a normal `Integer` on the Python side.

`class sqlalchemy.types.Boolean` typically uses `BOOLEAN` or `SMALLINT` on the DDL side.
For all backends, only the Python values `None`, `True`, `False`, `1` or `0` are accepted as parameter values.

`class sqlalchemy.types.Enum` provides a set of possible string values which the column is constrained towards.

Help on class Enum in module sqlalchemy.sql.sqltypes:

    class Enum(String, SchemaType)
     |  Generic Enum Type.
     |
     |  The :class:`.Enum` type provides a set of possible string values
     |  which the column is constrained towards.
     |
     |  The :class:`.Enum` type will make use of the backend's native "ENUM"
     |  type if one is available; otherwise, it uses a VARCHAR datatype and
     |  produces a CHECK constraint.

    import enum
    class MyEnum(enum.Enum):
        one = 1
        two = 2
        three = 3

    t = Table(
        'data', MetaData(),
        Column('value', Enum(MyEnum))
    )

    connection.execute(t.insert(), {"value": MyEnum.two})
    assert connection.scalar(t.select()) is MyEnum.two

Above, the string names of each element, e.g. “one”, “two”, “three”, are persisted to the database; the values of the Python Enum, here indicated as integers, are **not** used; the value of each enum can therefore be any kind of Python object whether or not it is persistable.

    class ColorSet(enum.Enum):
        one = 'red'
        two = 'green'

    class Department(Base):
        ...
        color = Column(Enum(ColorSet))

    it_department = Department(name='IT', color=ColorSet.two)

    dept_color = session.query(Department.color).filter(Department.id == 1).scalar()
    print(dept_color.value)
    # 'green'
    dept_color2 = session.query(Department.color).filter(Department.id == 1).one()
    print(dept_color2.color.value)
    # 'green'

`class sqlalchemy.types.Numeric`

     __init__(precision=None, asdecimal=False, decimal_return_scale=None, **kwargs)

A type for fixed precision numbers, such as `NUMERIC` or `DECIMAL`.
This type returns Python `decimal.Decimal` objects by default. Precision – the numeric precision for use in `DDL CREATE TABLE`.

`class sqlalchemy.types.Interval`

A type for `datetime.timedelta()` objects. In PostgreSQL, the native `INTERVAL` type is used; for others, the value is stored as a date which is relative to the “epoch” (Jan. 1, 1970).

`class sqlalchemy.types.LargeBinary`

Corresponds to a large and/or unlengthed binary type for the target platform, such as BLOB on MySQL and BYTEA for PostgreSQL. It also handles the necessary conversions for the DBAPI.

`class sqlalchemy.types.Time` - a type for datetime.time() objects.

SQL Value Processing: Augmenting Existing Types
-------------------------------------------------
The `TypeDecorator` allows the creation of custom types which add bind-parameter and result-processing behavior to an existing type object. It is used when additional in-Python marshaling of data to and from the database is required.

The class-level “impl” attribute is required, and can reference any `TypeEngine` class. With `TypeDecorator`, we are usually changing an incoming Python type to something new - `TypeDecorator` by default will “coerce” the non-typed side to be the same type as itself. Such as below, we define an “epoch” type that stores a date value as an integer:

    class MyEpochType(types.TypeDecorator):
        impl = types.Integer

        epoch = datetime.date(1970, 1, 1)

        def process_bind_param(self, value, dialect):
            return (value - self.epoch).days

        def process_result_value(self, value, dialect):
            return self.epoch + timedelta(days=value)

`class Comparator` includes the following, many of which are inherited from `ColumnOperator`

**`__eq__(other)`** implement the `==` operator. produces the clause `a = b`. If the target is `None`, produces `a IS NULL`.

**`__ne__(other)`** implements `!=` operator, gives clause `a != b`. If the target is `None`, produces `a IS NOT NULL`.

**`__le__(other)`, `__lt__(other)`** In a column context, produces the clause `a <= b` and `a < b`

**`between(cleft, cright, symmetric=False)`** gives `between()` clause against parent object from the lower and upper range.

**`concat(other)`** produces the clause `a || b`, or uses the `concat()` operator on MySQL.

**`contains(other, **kwargs)`, `endswith(other, **kwargs)`, `startswith(other, **kwargs)`**

    column LIKE '%' || <other> || '%'
    column LIKE '%' || <other>
    column LIKE <other> || '%'

    stmt = select([sometable]).\
        where(sometable.c.column.startswith("foobar"))

**`ilike(other, escape=None)`, `like(other, escape=None)`**

optional escape character, renders the ESCAPE keyword, e.g.:

    somecolumn.ilike("foo/%bar", escape="/")

**`in_(other)`**

produces the clause `column IN <other>`. The given parameter other may be:

A list of literal values, e.g.:

    stmt.where(column.in_([1, 2, 3]))

In this calling form, the list of items is converted to a set of bound parameters the same length as the list given:

    WHERE COL IN (?, ?, ?)

a `select()` construct, which is usually a correlated scalar select:

    stmt.where(
        column.in_(
            select([othertable.c.y]).
            where(table.c.x == othertable.c.x)
        )
    )

In this calling form, `ColumnOperators.in_()` renders as given:

    WHERE COL IN (SELECT othertable.y
    FROM othertable WHERE othertable.x = table.x)

A bound parameter, e.g. `bindparam()`, may be used if it includes the `bindparam.expanding` flag:

    stmt.where(column.in_(bindparam('value', expanding=True)))

In this calling form, the expression renders a special non-SQL placeholder expression that looks like:

    WHERE COL IN ([EXPANDING_value])

This placeholder expression is intercepted at statement execution time to be converted into the variable number of bound parameter form illustrated earlier. If the statement were executed as:

    connection.execute(stmt, {"value": [1, 2, 3]})

The database would be passed a bound parameter for each value:

    WHERE COL IN (?, ?, ?)

**`nullsfirst()`, `nullslast()`** provides clause of same name

**`bind_processor(dialect)`**

Provides a bound value processing function for the given Dialect.
This is the method that fulfills the `TypeEngine` contract for bound value conversion.

**`compile(dialect=None)`** is inherited from `TypeEngine` and when called with no arguments, uses a “default” dialect to produce a string result.

**`process_bind_param(value, dialect)`**

Subclasses override this method to return the value that should be passed along to the underlying `TypeEngine` object, and from there to the DBAPI `execute()` method.

The operation could be anything desired to perform custom behavior, such as transforming or serializing data. This could also be used as a hook for validating logic.

This operation should be designed with the reverse operation in mind, the `process_result_value` method.

Example:  some database connectors like those of SQL Server choke if a `Decimal` is passed with too many decimal places. Here’s a recipe that rounds them down:

    from sqlalchemy.types import TypeDecorator, Numeric
    from decimal import Decimal

    class SafeNumeric(TypeDecorator):
        """Adds quantization to Numeric."""

        impl = Numeric

        def __init__(self, *arg, **kw):
            TypeDecorator.__init__(self, *arg, **kw)
            self.quantize_int = - self.impl.scale
            self.quantize = Decimal(10) ** self.quantize_int

        def process_bind_param(self, value, dialect):
            if isinstance(value, Decimal) and \
                value.as_tuple()[2] < self.quantize_int:
                value = value.quantize(self.quantize)
            return value
