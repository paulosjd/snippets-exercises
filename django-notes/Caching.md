**Caching**

In dynamic websites, each user request for a page results in processing overhead including db queries, template rendering and business logic.
By saving results of expensive calculations, caching provides allows a web app to scale to handle more users.

Django offers different levels of cache granularity. It also works with 'downstream' caches which 
are not controlled directly but HTTP headers can be used specify what should be cached. These are systems which
cache before a request even reach your site. Examples include your ISP which may cache certain pages, proxy caches and web
browsers. They offer performance boosts but may blindly save pages based purely on URLs could expose incorrect or sensitive data to subsequent visitors to those pages. Therefore the correct HTTP headers need to be set.

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

**Cache access and invalidation**

The cache can be used through `cache.get()`, which takes a key and a default return value, and `cache.set()` which takes a key and a value. 
This could be used in the `get_object` method of a DetailView where you set the default queryset parameter to None (so a query is not made), check for an object with the cache key and return it if there is, else call `super` on the `get_object` method (and passing in a queryset) to get the object before calling `cache.set()` on it and returning it.

Cache invalidation is both very important but very difficult.
In order for a system of cache invalidation to be stateless,  only queries that we can effectively cache are ones that can be calculated on the basis of a single instance.
Fields on a model that uniquely identify an instance of that model can be used e.g. fields marked out as `unique=True` like `id`.
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
