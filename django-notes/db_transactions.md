Django’s default transaction behavior is to run in autocommit mode. Each query is immediately committed to the database, unless a transaction is active.
*the AUTOCOMMIT setting applies an implicit commit after each statement.*

According to SQL-92, “An SQL-transaction (sometimes simply called a “transaction”) is a sequence of executions of SQL-statements that is atomic with respect to recovery”. In other words, all the SQL statements are executed and committed together. Likewise, when rolled back, all the statements get rolled back together.
In the SQL standards, each SQL query starts a transaction, unless one is already active. Such transactions must then be explicitly committed or rolled back. e.g.:

    BEGIN TRANSACTION;

    UPDATE accounts
       SET balance = balance - 1000
     WHERE account_no = 100;

    UPDATE accounts
       SET balance = balance + 1000
     WHERE account_no = 200;

    INSERT INTO account_changes(account_no,flag,amount,changed_at)
    values(100,'-',1000,datetime('now'));

    INSERT INTO account_changes(account_no,flag,amount,changed_at)
    values(200,'+',1000,datetime('now'));

    COMMIT;

n.b. Some SQL statements cause an implicit commit. As a rule of thumb, such statements are Data definition language (DDL) statements.

The need to explicitly commit isn’t always convenient for application developers. To alleviate this problem, most databases provide an autocommit mode. When autocommit is turned on and no transaction is active, each SQL query gets wrapped in its own transaction. In other words, not only does each such query start a transaction, but the transaction also gets automatically committed or rolled back, depending on whether the query succeeded.

Django uses transactions or savepoints automatically to guarantee the integrity of ORM operations that require multiple queries, especially `delete()` and `update()` queries

**Example**: we want the two separate database statements to either both commit or both rollback

    cd = form.cleaned_data
    try:
        user = User.create(
            cd['name'], cd['email'],
            cd['password'], cd['last_4_digits'])

        if customer:
            user.stripe_id = customer.id
            user.save()
        else:
            UnpaidUsers(email=cd['email']).save()

    except IntegrityError:
        # ...

What happens if the `UnpaidUsers(email=cd['email']).save()` line fails?
You will have a user, registered in the system, that the system thinks has verified their credit card, but in reality they haven’t verified the card.

We only want one of two outcomes:

- The user is created (in the database) and has a stripe_id.

- The user is created (in the database) and doesn’t have a stripe_id AND an associated row in the UnpaidUsers table with the same email address is generated.

Atomic can be used as both a decorator or as a context_manager.

    try:
        with transaction.atomic():
            user = User.create(
                cd['name'], cd['email'],
                cd['password'], cd['last_4_digits'])

            if customer:
                user.stripe_id = customer.id
                user.save()
            else:
                UnpaidUsers(email=cd['email']).save()

    except IntegrityError:
        form.addError(cd['email'] + ' is already a member')

When `UnpaidUsers` fires the `IntegrityError` the `transaction.atomic()` context manager will catch it and perform the rollback. By the time our code executes in the exception handler the rollback will be done.

Atomicity is the defining property of database transactions. atomic allows us to create a block of code within which the atomicity on the database is guaranteed. If the block of code is successfully completed, the changes are committed to the database. If there is an exception, the changes are rolled back.

atomic is usable both as a decorator:

    @transaction.atomic
    def viewfunc(request):
        # This code executes inside a transaction.
        do_stuff()

and as a context manager:

    def viewfunc(request):
        # This code executes in autocommit mode (Django's default).
        do_stuff()
        with transaction.atomic():
            # This code executes inside a transaction.
            do_more_stuff()

Wrapping atomic in a try/except block allows for natural handling of integrity errors:

        @transaction.atomic
        def viewfunc(request):
            create_parent()

            try:
                with transaction.atomic():
                    generate_relationships()
            except IntegrityError:
                handle_exception()

            add_children()

In this example, even if `generate_relationships()` causes a database error by breaking an integrity constraint, you can execute queries in `add_children()`, and the changes from `create_parent()` are still there. Note that any operations attempted in `generate_relationships()` will already have been rolled back safely when `handle_exception()` is called, so the exception handler can also operate on the database if necessary.

In this mode Django will automatically wrap your view function in a transaction. If the function throws an exception Django will roll back the transaction, otherwise it will commit the transaction.

**Some general advice on using ORMs:**

Remember the ORM is an in-memory cache. ORMs can obscure bugs. Look at the SQL! Avoid read-modify-write
If you don't you'll probably need a lock.


**In-built locking**

Quoting the Django Docs, select_or_update():

Returns a queryset that will lock rows until the end of the transaction, generating a SELECT ... FOR UPDATE SQL statement on supported databases.

    games = Game.objects.select_for_update().filter(active=True)

All matched games will be locked until the end of the transaction block, meaning that other transactions will be prevented from changing or acquiring locks on them.

Usually, if another transaction has already acquired a lock on one of the selected rows, the query will block until the lock is released


**`F()` expressions**

An F() object represents the value of a model field or annotated column. It makes it possible to refer to model field values and perform database operations using them without actually having to pull them out of the database into Python memory.

Instead, Django uses the F() object to generate an SQL expression that describes the required operation at the database level. E.g. normally one might do this:

    reporter = Reporters.objects.get(name='Tintin')
    reporter.stories_filed += 1
    reporter.save()

Here, we have pulled the value of reporter.stories_filed from the database into memory and manipulated it using familiar Python operators, and then saved the object back to the database. But instead we could also have done:

    from django.db.models import F

    reporter = Reporters.objects.get(name='Tintin')
    reporter.stories_filed = F('stories_filed') + 1
    reporter.save()

Although reporter.stories_filed = F('stories_filed') + 1 looks like a normal Python assignment of value to an instance attribute, in fact it’s an SQL construct describing an operation on the database.

Whatever value is or was on reporter.stories_filed, Python never gets to know about it - it is dealt with entirely by the database. All Python does, through Django’s F() class, is create the SQL syntax to refer to the field and describe the operation.

To access the new value saved this way, the object must be reloaded:

    reporter = Reporters.objects.get(pk=reporter.pk)
    # Or, more succinctly:
    reporter.refresh_from_db()

As well as being used in operations on single instances as above, `F()` can be used on QuerySets of object instances, with `update()`. This reduces the two queries we were using above - the `get()` and the `save()` - to just one
We can also use `update()` to increment the field value on multiple objects - which could be very much faster than pulling them all into Python from the database, looping over them, incrementing the field value of each one, and saving each one back to the database:

    Reporter.objects.all().update(stories_filed=F('stories_filed') + 1)

`F()` therefore can offer performance advantages by:

    getting the database, rather than Python, to do work
    reducing the number of queries some operations require

**Avoiding race conditions using F()**

Another useful benefit of `F()` is that having the database - rather than Python - update a field’s value avoids a race condition.

If two Python threads execute the code in the first example above, one thread could retrieve, increment, and save a field’s value after the other has retrieved it from the database. The value that the second thread saves will be based on the original value; the work of the first thread will simply be lost.

If the database is responsible for updating the field, the process is more robust: it will only ever update the field based on the value of the field in the database when the `save()` or `update()` is executed, rather than based on its value when the instance was retrieved.

Imagine you’ve got an online bookstore application with a Book  model that has a quantity attribute. When somebody buys a copy of one of your books, you want to decrease the quantity attribute by 1. Here is the naive way to do it:

    book = Book.objects.get(id=12)
    book.quantity -= 1
    book.save()

Now imagine your bookstore grows, you open some new branches, and there are multiple updates being run on your application every second. That’s when strange things will start to happen. Here is how two concurrent updates might play out with our current code. book1 represents the first concurrent update and book2 represents the second:

    book1 = Book.objects.get(id=12)
    book2 = Book.objects.get(id=12)
    book1.quantity -= 1
    book2.quantity -= 1
    book1.save()
    book2.save()

At the start of both concurrent updates, an identical copy of the data in the database is loaded into memory.  The inventory quantity is decreased on each copy, then the new quantity is written back to the database. The result being as if one of the updates never happened. Avoid using:

    book = Book.objects.get (id=12)
    book = F("quantity") -1
    book.save ()
