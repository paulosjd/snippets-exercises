**How Django knows to UPDATE vs. INSERT**

Django database objects use the same `save()` method for creating and changing objects. Django abstracts the need to use `INSERT` or `UPDATE` SQL statements. Specifically, when you call `save(`), Django follows this algorithm:

If the object’s primary key attribute is set to a value that evaluates to `True` (i.e., a value other than None or the empty string), Django executes an `UPDATE`.

If the object’s primary key attribute is not set or if the `UPDATE` didn’t update anything, Django executes an `INSERT`.
