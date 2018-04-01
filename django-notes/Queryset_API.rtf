**When queries are executed**

Simply creating querysets does not involve any database activity. No database activity actually occurs until you do something to evaluate the queryset. Evaluation can be forced in the following ways: 

- Iterating over it
- Calling len() or list() on it
- Slicing it with the ‘step’ parameter* 
- Testing it in a boolean context*

Note that once a queryset has been sliced, no further filtering may take place. Also, for testing the queryset in an if statement, the most efficient way to check for object membership using a unique field (e.g. primary key) is to use `exists()`.


Equally, instead of calling `len()` on the queryset, use `count()`.A simple example of avoiding unnecessary evaluations:

How data is held in memory
When a queryset is created the cache is empty. When it is evaluated and database interaction occurs, the results of the query are stored and the requested results are returned.

In many cases the queryset should be stored and re-used instead of consuming:

    entry = Entry.objects.get(id=1)
    entry.blog  # Blog object is retried
    entry.blog  # cached version, no DB lookup
    
    entry.authors.all()    #query performed
    entry.authors.all()    #query performed again

In general, callables will results in and DB query being performed, whereas attributes of ORM objects will be cached.
select_related is useful for optimization DB operations:

    class Album(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    
    Song(models.Model):
    name = models.CharField(max_length=50)
    album = models.ForeignKey(Album)
    
    song = Song.objects.get(id=5) # query performed
    
    album =  song.album # query performed again
    
    Only one db lookup needed: 
    
    song = Song.objects.select_related(‘album’).get(id=5)
    
    # song.album # database query not required

As caching objects can involve significant memory usage, if the queryset will not need to be re-used sometimes then there is no need for it to be cached.
Dont’ get things you don’t need. Using `QuerySet.values()` or `values_list()` is useful where when you just need a dictionary or a list of the values, not the ORM model objects. 

**Methods that return new QuerySets**

QuerySet refinement methods:

    filter(**kwargs) Returns a new QuerySet containing objects that match the given lookup parameters.

    exclude(**kwargs) Returns a new QuerySet containing objects that do not match the given lookup parameters.
    
    annotate(*args, **kwargs) Each argument to annotate() is an annotation that will be added to each object in the QuerySet that is returned.

You may want to determine how many entries have been made in each blog: 

    >>> from django.db.models import Count
    >>> q = Blog.objects.annotate(Count('entry'))
    >>> q[0].name
    'Blogasaurus'
    >>> q[0].entry__count
    42

The Blog model doesn’t define an entry__count attribute by itself, but by using a keyword argument to specify the aggregate function, you can control the name of the annotation:

    >>> q = Blog.objects.annotate(number_of_entries=Count('entry'))
    >>> q[0].number_of_entries
    42

    order_by(*fields) You can override the ordering in the model’s Meta on a per-QuerySet basis

Each field you add to the ordering incurs a cost to your database. To order by a field in a different model, use the same syntax as when you are querying across model relations:

    Entry.objects.order_by('blog__name', 'headline')
    
Note that ordering is not a free operation. 
    
    reverse() use this method to reverse the order in which a queryset’s elements are returned
    
To retrieve the “last” five items in a queryset, you could do the following:
    
    my_queryset.reverse()[:5]
 
Note that this is not the same as slicing from the end of a sequence in Python 
since the penultimate item is returned first and so on. 
Django doesn’t support that mode of access (slicing from the end), because it’s not possible to do it efficiently in SQL
    
    distinct(*fields) uses SELECT DISTINCT in its SQL query which eliminates duplicate rows from the query results.
 
Simple queries such as Blog.objects.all() don’t introduce the possibility of duplicate result rows. However, if your query spans multiple tables, it’s possible to get duplicate results when a QuerySet is evaluated. That’s when you’d use distinct(). 
    
    values(*fields, **expressions) Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.
    
    >>> Blog.objects.filter(name__startswith='Beatles')
    <QuerySet [<Blog: Beatles Blog>]>
    >>> Blog.objects.values()
    <QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
    >>> Blog.objects.values('id', 'name')
    <QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>

The `values()` method also takes optional keyword arguments, **expressions, which are passed through to `annotate()`:

    >>> from django.db.models.functions import Lower
    >>> Blog.objects.values(lower_name=Lower('name'))
    <QuerySet [{'lower_name': 'beatles blog'}]>


    values_list(*fields, flat=False, named=False) is similar to values() except instead it returns tuples when iterated over.

    >>> Entry.objects.values_list('id', 'headline')
    <QuerySet [(1, 'First entry'), ...]>

If you only pass in a single field, you can also pass in the flat parameter. If True, this will mean the returned results are single values, rather than one-tuples:

    >>> Entry.objects.values_list('id').order_by('id')
    <QuerySet[(1,), (2,), (3,), ...]>
    
    >>> Entry.objects.values_list('id', flat=True).order_by('id')
    <QuerySet [1, 2, 3, ...]>

A common need is to get a specific field value of a certain model instance. To achieve that, use `values_list()` followed by a `get()` call:

    >>> Entry.objects.values_list('headline', flat=True).get(pk=1)
    'First entry'
    
`values()` and `values_list()` are both intended as optimizations for a specific use case: retrieving a subset of data without the overhead of creating a model instance. This metaphor falls apart when dealing with many-to-many and other multivalued relations (such as the one-to-many relation of a reverse foreign key) because the “one row, one object” assumption doesn’t hold.
    
    dates(field, kind, order='ASC') Returns a QuerySet that evaluates to a list of datetime.date objects of available dates of a particular kind within the contents of the QuerySet.
 
    datetimes(field_name, kind, order='ASC', tzinfo=None) Similar to the above, giving list of datetime.datetime objects
    
field should be the name of a DateField of your model. kind should be either "year", "month" or "day" (also "hour", "minute" or "second" are allowed for datetimes).
  
     all() Returns a copy of the current QuerySet (or QuerySet subclass). 

This can be useful in situations where you might want to pass in either a model manager or a QuerySet and do further filtering on the result. 
When a QuerySet is evaluated, it typically caches its results.   
    
     select_related(*fields) Returns a QuerySet that will “follow” FK relationships, selecting additional related-object data
       
This is a performance booster which results in a single more complex query but means later use of foreign-key relationships won’t require database queries.
    
    b = Book.objects.select_related('author__hometown').get(id=4)    # Hits the database.
    p = b.author         # Doesn't hit the database.
    c = p.hometown       # Doesn't hit the database.
    
    b = Book.objects.get(id=4)  # Hits the database.
    p = b.author         # Hits the database.
    c = p.hometown       # Hits the database.   
    
Chaining `select_related` calls works in a similar way to other methods:

select_related('foo', 'bar') is equivalent to 

select_related('foo').select_related('bar')

    prefetch_related(*lookups) Returns a QuerySet that will automatically retrieve related objects for each specified lookups.
    
This has a similar purpose to `select_related`, but the strategy is quite different

`select_related` works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query. However, to avoid the much larger result set that would result from joining across a ‘many’ relationship, select_related is limited to FK and one-to-one relationships.

`prefetch_related`, on the other hand, does a separate lookup for each relationship, and does the ‘joining’ in Python. This allows it to prefetch many-to-many and many-to-one objects, which cannot be done using `select_related`, in addition to the foreign key and one-to-one relationships that are supported by `select_related`. 

It also supports prefetching of GenericRelation and GenericForeignKey, however, it must be restricted to a homogeneous set of results. E.g. prefetching objects referenced by a GenericForeignKey is only supported if the query is restricted to one ContentType. Consider the following:

    class Topping(models.Model):
        name = models.CharField(max_length=30)

    class Pizza(models.Model):
        name = models.CharField(max_length=50)
        toppings = models.ManyToManyField(Topping)
    
        def __str__(self):
            return "{} {}".format(self.name,
                ", ".join(topping.name for topping in self.toppings.all()),)
    
    >>> Pizza.objects.all()
    ["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)"...

The problem with this is that every time Pizza.__str__() asks for self.toppings.all() it has to query the database, so Pizza.objects.all() will run a query on the Toppings table for every item in the Pizza QuerySet.

We can reduce to just two queries using prefetch_related:

    >>> Pizza.objects.all().prefetch_related('toppings')
   
This implies a self.toppings.all() for each Pizza; now each time self.toppings.all() is called, instead of having to go to the database for the items, it will find them in a prefetched QuerySet cache that was populated in a single query.

Remember that, as always with QuerySets, any subsequent chained methods which imply a different database query will ignore previously cached results, and retrieve data using a fresh database query. So, if you write the following:

    >>> pizzas = Pizza.objects.prefetch_related('toppings')
    >>> [list(pizza.toppings.filter(spicy=True)) for pizza in pizzas]
    
…then the fact that pizza.toppings.all() has been prefetched will not help you. The prefetch_related('toppings') implied pizza.toppings.all(), but pizza.toppings.filter() is a new and different query. The prefetched cache can’t help here; in fact it hurts performance, since you have done a database query that you haven’t used. So use this feature with caution!

**Methods that do not return QuerySets**

The following QuerySet methods evaluate the QuerySet and return something other than a QuerySet.
These methods do not use a cache and they query the database each time they’re called.

    get(**kwargs) Returns the object matching the given lookup parameters
     
    entry = Entry.objects.filter(...).exclude(...).get()
    
Raises MultipleObjectsReturned if more than one object was found or a DoesNotExist exception if an object wasn’t found.
If you expect a queryset to return one row, you can use get() without any arguments to return the object for that row.
      
    create(**kwargs) A convenience method for creating an object and saving it all in one step 
    
    get_or_create(defaults=None, **kwargs) A convenience method for looking up an object, creating one if necessary.   
    
These are meant as a shortcut for  boilerplate-ish code involving try/except block. 
When using these methods in Django views, be sure to use it only in POST requests unless you have a good reason not to. GET requests shouldn’t have any effect on data. Instead, use POST whenever a request to a page has a side effect on your data.
    
    bulk_create(objs, batch_size=None) This method inserts the provided list of objects into the database in an efficient manner:
    
    >>> Entry.objects.bulk_create([
    ...     Entry(headline='This is a test'),
    ...     Entry(headline='This is only a test'),
    ... ])
    
This has a number of caveats though. 
  
    count() Returns an integer representing the number of objects in the database matching the QuerySet. 
    
The `count()` method never raises exceptions. A `count()` call performs a `SELECT COUNT(*)` behind the scenes, so you should always use `count()` rather than loading all of the record into Python objects and calling `len()` on the result (unless you need to load the objects into memory anyway, in which case `len()` will be faster).

Note that if you want the number of items in a QuerySet and are also retrieving model instances from it (for example, by iterating over it), it’s probably more efficient to use `len(queryset)`  which won’t cause an extra database query like `count()` would.

    latest(*fields) Returns the latest object in the table based on the given field(s).

    earliest(*fields) Works the same as latest(), but direction changed

This example returns the latest Entry in the table, according to the pub_date field:

    Entry.objects.latest('pub_date')
    ---
    first() Returns the first object matched by the queryset, or None if there is no matching object
    
    last() Works like first(), but returns the last object
    
Note that `first()` is a convenience method, the following code sample is equivalent to the above example:
    
    try:
        p = Article.objects.order_by('title', 'pub_date')[0]
    except IndexError:
        p = None
    ---
    aggregate(*args, **kwargs) -Returns a dictionary of aggregate values (averages, sums, etc.) calculated over the QuerySet.

Since aggregates are also query expressions, you may combine aggregates with other aggregates or values to create complex aggregates.
By using a keyword argument to specify the aggregate function, you can control the name of the aggregation value that is returned.

    >>> from django.db.models import Count
    >>> q = Blog.objects.aggregate(Count('entry'))
    {'entry__count': 16}
    >>> q = Blog.objects.aggregate(number_of_entries=Count('entry'))
    {'number_of_entries': 16}

    exists() Returns True if the QuerySet contains any results, and False if not. 

`exists()` is useful for searches relating to object existence in or membership in a QuerySet, particularly in the context of a large QuerySet.
It will be faster than evaluating a queryset and iterating through it as for a conditional if statement.

    update(**kwargs) Performs an SQL update query for the specified fields, and returns the number of rows matched

The `update()` method is applied instantly, and the only restriction on the QuerySet that is updated is that it can only update columns in the model’s main table, not on related models.
Filtering based on related fields is still possible, though. If you’re just updating a record and don’t need to do anything with the model object, the most efficient approach is to call update(), rather than loading the model object into memory.

Using `update()` also prevents a race condition wherein something might change in your database in the short period of time between loading the object and calling `save()`.

Finally, realize that `update()` does an update at the SQL level and, thus, does not call any `save()` methods on your models, nor does it emit the pre_save or post_save signals (which are a consequence of calling `Model.save()`)

    delete() Performs an SQL delete query on all rows in the QuerySet and returns data relating to the deletions

By default, Django’s ForeignKey emulates the SQL constraint ON DELETE CASCADE — in other words, any objects with foreign keys pointing at the objects to be deleted will be deleted along with them.
This cascade behavior is customizable via the on_delete argument to the ForeignKey.

The `delete()` method does a bulk delete and does not call any `delete()` methods on your models. It does, however, emit the pre_delete and post_delete signals for all deleted objects (including cascaded deletions).

    as_manager() Class method that returns an instance of Manager with a copy of the QuerySet’s methods.

**Field lookups**

Field lookups are how you specify the meat of an SQL `WHERE` clause. They’re specified as keyword arguments to the QuerySet methods `filter()`, `exclude()` and `get()`.

    Entry.objects.get(id__exact=14)
    Blog.objects.get(name__iexact='beatles blog')    #Case-insensitive 
    Entry.objects.get(headline__contains='Lennon')
    Entry.objects.get(headline__icontains='Lennon')    #Case-insensitive 
    Entry.objects.filter(id__in=[1, 3, 4])    # iterable can be a QuerySet
    Entry.objects.filter(id__gt=4)
    
gte, lt, lte, startswith, regex, date, month, day etc.




    
    