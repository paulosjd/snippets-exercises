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

**django.utils.decorators**

`@method_decorator`

Transforms a function decorator into a method decorator so that it can be used on an instance method. For example:

    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator

    class ProtectedView(TemplateView):
        template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

**django.utils.http**

HTTP URLs may be Base64 encoded not for security reasons, but for application reasons, specific to that web server. Base64 encoding schemes are commonly used when there is a need to encode binary data that needs be stored and transferred over media that are designed to deal with textual data. This is to ensure that the data remains intact without modification during transport. Base64 schemes represent binary data in an ASCII string format (English alphabet, common punctuation chars, control chars) by translating it into a base-64 representation.


`urlsafe_base64_encode(s)` Encodes a bytestring in base64 for use in URLs, stripping any trailing equal signs.

`urlsafe_base64_decode(s)`  Decodes a base64 encoded string, adding back any trailing equal signs that might have been stripped.

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


**django.utils.text**

`slugify(unicode=False)`

Converts spaces to hyphens. Removes characters that aren’t alphanumerics, underscores, or hyphens. Converts to lowercase.
Also strips leading and trailing whitespace.

    >>> slugify("Joel is a slug")
    joel-is-a-slug

    >>> slugify("你好 World", allow_unicode=True)
    你好-world

**django.utils.timezone**

`now()`

Returns a datetime for the current time in UTC. The value of USE_TZ determines if it is aware.

`localtime(value=None, timezone=None)`

Converts an aware datetime to a different time zone, by default the current time zone.

