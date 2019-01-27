    psql -U username -d mydatabase -c 'SELECT * FROM mytable'

The rule of thumb is: If you received no response from psql but you were expecting at least SOMETHING, then you forgot the semicolon ;

Initiate an interactive session:

    psql -U username mydatabase
    mydatabase=#

At this point you can enter a query directly but you must remember to terminate the query with a semicolon ;

For example:

    mydatabase=# SELECT * FROM mytable;

**Connect to PostgreSQL database**

The following command connects to a database under a specific user. After pressing Enter PostgreSQL will ask for the password of the user.

    psql -d database -U  user -W

For example, to connect to dvdrental database under postgres user, you use the following command:

    C:\Program Files\PostgreSQL\9.5\bin>psql -d dvdrental -U postgres -W
    Password for user postgres:
    dvdrental=#

If you want to connect to a database that resides on another host, you add the -h option as follows:

    psql -h host -d database -U user -W

In case you want to use SSL mode for the connection, just specify it in the command as the following command:

    psql -U user -h host "dbname=db sslmode=require"

Switch connection to a new database

Once you are connected to a database, you can switch the connection to a new database under a user specified by user. The previous connection will be closed. If you omit the user parameter, the current user is assumed.

    \c dbname username

The following command connects to dvdrental database under postgres user:

    postgres=# \c dvdrental
    You are now connected to database "dvdrental" as user "postgres".
    dvdrental=#

**List available databases**

To list all databases in the current PostgreSQL database server, you use \l command:

    \l

**List available tables**

To list all tables in the current database, you use \dt command:

    \dt

Note that this command shows only table in the current connected database.
Describe a table

To describe a table such as a column, type, modifiers of columns, etc., you use the following command:

    \d table_name

**List available schema**

To list all schema of the currently connected database, you use the \dn command.

    \dn

**List available functions**

To list available functions in the current database, you use the \df command.

    \df

**List available views**

To list available views in the current database, you use the \dv command.

    \dv

**List users and their roles**

To list all users and their assign roles, you use \du command:

    \du

**Execute the previous command**

To retrieve the current version of PostgreSQL server, you use the version() function as follows:

    SELECT version();

Now, you want to save time typing the previous command again, you can use \g command to execute the previous command:

    \g

psql executes the previous command again, which is the SELECT statement,.

**Get help on psql commands**

To know all available psql commands, you use the `\?` command.
1

    \?

To get help on specific PostgreSQL statement, you use the \h command.

For example, if you want to know detailed information on ALTER TABLE statement, you use the following command:

    \h ALTER TABLE

**Turn on query execution time**

To turn on query execution time, you use the \timing command.

    dvdrental=# \timing
    Timing is on.
    dvdrental=# select count(*) from film;
     count
    -------
      1000
    (1 row)

    Time: 1.495 ms
    dvdrental=#

You use the same command \timing to turn it off.

    dvdrental=# \timing
    Timing is off.
    dvdrental=#