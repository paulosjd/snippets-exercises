from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey

metadata = MetaData()

user = Table('user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(16), nullable=False),
    Column('email_address', String(60)),
    Column('password', String(20), nullable=False)
)

print(dir(metadata))

employees = Table('departments', metadata,
    Column('department_id', Integer, primary_key=True),
)

employees = Table('employees', metadata,
    Column('employee_id', Integer, primary_key=True),
    Column('employee_name', String(60), nullable=False),
    Column('employee_dept', Integer, ForeignKey("departments.department_id"))
)

# for c in employees.columns
for c in employees.c:
    print(c)



print(dir(employees.columns.employee_id))
employees.c.employee_name.key = 'foobar'
print(employees.c.employee_name.key)
print(list(employees.c.employee_dept.foreign_keys)[0].column.table)


