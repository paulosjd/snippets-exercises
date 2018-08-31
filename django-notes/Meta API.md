The Meta API hidden under under the _meta object within each model, which Django uses it to introspect a models internals. I is essential to the Django ORM,  ModelForms, the admin and migrations.  Third-party applications such as Django-Rest-Framework also rely on it and even before it was formalized in Django 1.10, developers had needed to use it despite being an internal API.

The Meta object provides metadata about the model such as the model name, the name of the app it is registered in, database table name and the primary key field.  It also provides metadata about the fields and relations of a model. The new Meta API was designed to be used by developers without fear of breakage, as well as being easy to use and intuitive. It was simplified to provide to main ‘entry points’:  get_field() and get_fields() which are the ‘shortcuts’ identified by its creators. 

get_field() returns the field instance given a name of a field 

The field name may be a field defined on another model that points to the model (a ManyToOneRel). A distinction is made between fields defined on the model and related objects (the ‘other side’ of a ForeignKey relation, or either side of a ManyToManyField relation). 

get_fields() returns a tuple of fields associated with a model:

 
get_fields  - a single generator funciton that contains all the logic about where to search for fields

designed to be fast – since whole django system relies upon it. Values will be pre-computed upon initialiatizing and held within a cache e.g. return from get_fields()… these are the ‘shortcuts’ identified by its creators.
a centralized cache and a centralized cache invalidation

get_fields is the main method that iterates through all the models, handling inheritance and so. In every loop through a model, the result is cached, leading to more performance.
For related objects, a complete graph of all the models with all the fields is needed. This is an expensive one-time operation which is cached afterwards.
Sidenote: what is used often in Meta is the cached_property decorator. It is a property that is only computed once per instance. It prevents lots of unnecessary re-calculations.
cached_property is included in django. You can also install a generic implementation from https://github.com/pydanny/cached-property (Note: at the bottom of the README there, I get thanked for calling cached_property to pydanny’s (Daniel Greenfeld’s) attention. Funny :-) )
Cached_property means the five extra cached properties (for grabbing related objects, for instance) are essentially free. They don’t have any overhead as they’re computed only once.
An important concept in the Meta API: immutability. This helps prevents lots of bugs. If you return an immutable result, you can be sure it cannot be changed (of course). An advantage is that they’re quick. You can also use itertools.chain() to avoid allocating a new list. You can make a copy of everything as a list, of course.