CHange to caching??


**django.utils.cache**

This module contains helper functions for controlling caching. It does so by managing the Vary header of responses.
Essentially, the Vary HTTP header defines which headers a cache should take into account when building its cache key. Requests with the same path but different header content for headers named in Vary need to get different cache keys to prevent delivery of wrong content.

   The "Vary" header field in a response describes certain parts of a
   request that might have a role in selecting the
   representation. e.g. 
     Vary: accept-encoding, accept-language
   indicates that the origin server might have used the request's
   Accept-Encoding and Accept-Language fields (or lack thereof) as
   determining factors while choosing the content for this response.
   
   
   
**django.utils.functional**
   
`@cached_property`

A decorator that can be used in place of the standard `@property` decorator so that the result of the property function is cached on the instance.
It is useful for improving performance by avoiding unnecessary computation or requests to external services such as a database or web API. 
Also, it can ensure that an attribute’s value does not change unexpectedly over the life of an instance. Consider the following example:

    class Person(models.Model):
    
        def friends(self):
            # expensive computation
            ...
            return friends

You may end up calling the method multiple times across your views and templates, each time requiring the value to be computed.
This may be avoided by decorating the method with `@cached_property`:

    class Person(models.Model):

        @cached_property
        def friends(self):
            ...
It is effectively a shortcut for writing something like:

    @property
    def friends(self):
        if self._friends is None:
            self._friends = self.get_friends()
        return self._friends

The cached result will persist as long as the instance does. The cached value can be treated like an ordinary attribute of the instance, allowing it to be cleared:

    a = person.friends         # calls first time
    b = person.get_friends()   # calls again
    c = person.friends         # does not call
    a is c                     # is True 
    del person.friends         # clear it, requiring re-computation next time it's called

**django.utils.safestring**

Functions and classes for working with “safe strings”: strings that can be displayed safely without further escaping in HTML.

`class SafeText` 
 
A str subclass that has been specifically marked as “safe” for HTML output purposes.

`mark_safe(s)`

Can also be used as a decorator. String marked safe will become unsafe again if modified. For example:

    >>> mystr = '<b>Hello World</b>   '
    >>> mystr = mark_safe(mystr)
    >>> type(mystr)
    <class 'django.utils.safestring.SafeText'>
    
    >>> mystr = mystr.strip()  # removing whitespace
    >>> type(mystr)
    <type 'str'>




      
    
