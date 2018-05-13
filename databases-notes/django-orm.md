**How Django knows to UPDATE vs. INSERT**

Django database objects use the same `save()` method for creating and changing objects. Django abstracts the need to use `INSERT` or `UPDATE` SQL statements. Specifically, when you call `save(`), Django follows this algorithm:

If the object’s primary key attribute is set to a value that evaluates to `True` (i.e., a value other than None or the empty string), Django executes an `UPDATE`.

If the object’s primary key attribute is not set or if the `UPDATE` didn’t update anything, Django executes an `INSERT`.

**In-built locking**

Remember the ORM is an in-memory cache. ORMs can obscure bugs. Look at the SQL! Avoid read-modify-write
If you don't you'll probably need a lock.

Quoting the Django Docs, `select_or_update()`:

Returns a queryset that will lock rows until the end of the transaction, generating an SQL statement on supported databases.

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


