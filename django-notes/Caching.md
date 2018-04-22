In dynamic websites, each user request for a page results in processing overhead including db queries, template rendering and business logic.
By saving results of expensive calculations, caching provides allows a web app to scale to handle more users.

Django offers different levels of cache granularity. It also works with 'downstream' caches which 
are not controlled directly but HTTP headers can be used specify what should be cached. These are systems which
cache before a request even reach your site. Examples include your ISP which may cache certain pages, proxy caches and web
browsers. They offer performance boosts but may blindly save pages based purely on URLs could expose incorrect or sensitive data to subsequent visitors to those pages. Therefore the correct HTTP headers need to be set.

**Caching backends**

Your cache preference goes in the CACHES setting in your settings file.  The two main caching backends are Memcached and Redis. 
Memcached, a memory-based cache server, runs as a daemon and is allotted a specified amount of RAM. It simply provides an interface for data in the cache, which is stored directly in memory so avoids I/O overhead.
Redis is a common database cache and can be installed using AWS ElastiCache. To set up, the LOCATION value is set to the name of the db table which you create using a Django management command.

    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000 }}}

Other additional keys in the CACHES setting include TIMEOUT (seconds before cache keys expire) and MAX_ENTRIES (entries allowed in the cache before old values are deleted). The default cache is local-memory caching which is not recommended for production but is useful in development.

Once the cache is set up, certain middleware needs to be added along with the required settings. 
The simplest caching strategy is to set up caching to cache the entire site.
View can still set their own cache expiry time such as using the `cache control()` decorator.
A more granular way to use the caching framework is by caching the output of individual views. This can be done using
the `cache_page` decorator that will automatically cache a view’s response; it take a single argument, the cache timeout in seconds.

Cache invalidation
==================
The cache can be used through `cache.get()`, which takes a key and a default return value, and `cache.set()` which takes a key and a value.
This could be used in the `get_object` method of a DetailView where you set the default queryset parameter to None (so a query is not made), check for an object with the cache key and return it if there is, else call `super` on the `get_object` method (and passing in a queryset) to get the object before calling `cache.set()` on it and returning it.
Cache invalidation is both very important but very difficult.

**Why you can’t invalidate open-ended queries**

Take the example of this simple query:

    from django.core.cache import cache

    def cached_get_things_older_than(age):
        """Return things older than the specified age"""
        key = SOME_CACHE_KEY.format(age)
        result = cache.get(key)
        if result is None:
            result = MyModel.objects.filter(age__gt=age)
            cache.set(key, result, SOME_CACHE_TIMEOUT)
        return result

In order for this code to be correct all of the time, you need to invalidate the cache whenever the data changes in a way that make the cached value inaccurate.
Many things would invalidate any of this cached data: a new thing with an age > 20 is added or deleted. a thing < or > 20 is changed to > or < 20. a thing again to > 20.
Hopefully, you can already see that invalidation of even this simplest of simple open-ended queries is a non-trivial task.

OK, so we could use some signal handlers, perhaps like this:

    from django.db.models.signals import pre_save, post_save, post_delete

    def pre_save_thing(sender, instance, **kwargs):
        if not instance.id:
            return
        old_instance = MyModel.objects.get(id=instance.id)
        old_instance_older_than_20 = bool(old_instance.age > 20)
        instance_older_than_20 = bool(instance.age > 20)
        if old_instance_older_than_20 != instance_older_than_20:
            invalidate_cache(20)

    def post_save_thing(sender, instance, created,  **kwargs):
        if created and instance.age > 20:
            invalidate_cache(20)

    def post_delete_thing(sender, instance, **kwargs):
        if instance.age > 20:
            invalidate_cache(20)

    pre_save.connect(pre_save_thing, sender=MyModel)
    post_save.connect(post_save_thing, sender=MyModel)
    post_delete.connect(post_delete_thing, sender=MyModel)

This is a lot of work to invalidate even the simplest one-parameter query, and doesn't even cover everything.
In order to correctly invalidate these open-ended queries, you’re going to have to remember what queries you’ve run in the past, store them somewhere, and each time something in the data changes, pull down this stored list of queries, go through them all and invalidate any queries that have been affected by the data change.
This is unscalable and utterly unworkable for the vast majority of sites where data is read from and written to frequently.
Therefore any system of cache invalidation must be stateless.

**What queries can we cache?**

In order for a system of cache invalidation to be stateless, the only queries that we can effectively cache are ones that can be calculated on the basis of a single instance:

Fields on a model that uniquely identify an instance of that model can be used e.g. fields marked out as `unique=True` like `id`.

We can also use partial-keys that appear in unique_together constraints in the model definition.

We can also always invalidate the `all() query if we need to too. Like Johnny Cache (“whenever anything in a table of data changes, invalidate ALL cached query data originating from that table” - useless for frequently changing (volatile) data, we can, without any overhead, categorically say that any change to any model will invalidate the `all()` query for that model.

**what else should i be aware of?**

Calling `cache.delete(key)` with a constructed key is a typical way to invalidate cache-keys in response to signal-handlers firing as a result of model-instance save/delete.

Complexity within the query-space of a single model’s fields (intra-model complexity) is one thing, but what about inter-model complexity.
Consider this example:

    class Parent(models.Model):
        name = models.CharField(max_length=100)
     
    class Child(models.Model):
        name = models.CharField(max_length=100)
        mother = models.ForeignKey(Parent)
        father = models.ForeignKey(Parent)
    
    def cached_get_child(child_id):
        key = CHILD_CACHE_KEY.format(child_id)
        child = cache.get(key)
        if child is None:
            child = Child.objects.select_related('mother', 'father').get(id=child_id)
            cache.set(key, child, CHILD_CACHE_TIMEOUT)
        return child

The caching of the Child object above using the id field is fine. It is the primary-key of the Child model, we can easily hook up signal-handlers to invalidate the cached value on save/delete. However, when storing the Child value into the cache, we’re also storing a copy of the Child's Parents as we do so by using `select_related()`. In order to correctly invalidate the data in the cache, we also need to hook up signal-handlers for the Parent model and invalidate any Child of a Parent when the Parent instance changes. In this simple example above, this is still relatively easy to do.
However, suppose you cache a model ModelA that relates to ModelB, than in turn relates to ModelC, and so on. Suppose the cached data does `select_related()` on this chain of model-relations. See how the cache invalidation complexity linearly increases with model-relation-depth. It will quickly become unworkable in the same way as the open-ended queries.
Some rules:

    #1: any system of invalidation must be stateless.
    #2: as a result of rule #1, only cache-keys that directly relate to an individual model-instance can be cached.
    #3: all() can also be cached and invalidated without any need for complex invalidation logic.
    #4: only ever cache the model-instance that the cache-key relates to in the cache. Never cache related-objects that do not directly relate to the cache-key that the data is being stored under.

Specific requirements/goals that the implementation in the caching app should fulfil:

    Follow the fundamental rules outlined above.
    Automate the process of caching, cache invalidation and best-practices for cache-key construction outlined above. Prevent the need for developers to write vast swathes of boiler-plate code.
    Cache-invalidation should be O(1) complexity and not adversely affect performance of the system in any way.
    Data returned from the caching functionality should be correct above all other considerations. Cached data must be invalidated when appropriate.
    Caching of model-instances should [greatly] reduce load on the database for the simpler queries.
    Retrieving cached model-instance from the cache should improve performance over and above using the database directly. As a bare minimum, it should at least match the performance of the database!
    Introducing caching functionality into a particular model should automatically accelerate any related fields in other models that point to the cached model.
    Caching should be tightly integrated into the Django ORM used to make database queries. Developers should not have to write anything other than standard Django ORM-query code.
    As a result of the above point, the caching functionality should be able to be dropped into an existing project with no caching with very little modification to any of the code that performs Django ORM queries.
    The particulars of what can or cannot be cached should be abstracted away from the developer and left to the caching app author to decide what is best/correct. Developers need not be an expert to employ caching on their projects.
    In this way, most (if not all) caching code is centralized in (and fixable from) a single location.

**django.utils.cache**

This module contains helper functions for controlling caching, by managing the `Vary` header of responses.

The `Vary` header defines which request headers a cache mechanism should take into account when building its cache key.
This informs cache recipients where this response can be used to satisfy later requests.
For example, if the contents of a Web page depend on a user’s language preference, the page is said to “vary on language.”

     Vary: accept-encoding, accept-language

By default, Django’s cache system creates cache keys using the requested fully-qualified URL. This means every request to that URL will use the same cached version, regardless of user-agent differences such as cookies or language preferences. However, if this page produces different content based on some difference in request headers – such as a cookie, or a language, or a user-agent – you’ll need to use the `Vary` header to tell caching mechanisms that the page output depends on those things.
To do so:

    @vary_on_headers('User-Agent')
    def my_view(request):
        ...
This tells downstream caches to produce different content based on some difference in request headers – such as a cookie, or a language, or a user-agent
This means each combination of e.g. user-agent and cookie will get its own cache value.

Template Caching
================
Django’s template system will read and compile a template every time it is rendered. This happens quickly, but when you render multiple templates on each page it can add up