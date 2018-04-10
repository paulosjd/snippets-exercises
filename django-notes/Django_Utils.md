CHange to caching??


django.utils.cache

This module contains helper functions for controlling caching. It does so by managing the Vary header of responses.
Essentially, the Vary HTTP header defines which headers a cache should take into account when building its cache key. Requests with the same path but different header content for headers named in Vary need to get different cache keys to prevent delivery of wrong content.

   The "Vary" header field in a response describes certain parts of a
   request that might have a role in selecting the
   representation. e.g. 
     Vary: accept-encoding, accept-language
   indicates that the origin server might have used the request's
   Accept-Encoding and Accept-Language fields (or lack thereof) as
   determining factors while choosing the content for this response.