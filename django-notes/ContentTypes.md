Django includes a contenttypes application that can track all of the models installed in your Django-powered project, providing a high-level, generic interface for working with your models.

At the heart of the contenttypes application is the `ContentType` model, which lives at django.contrib.contenttypes.models.ContentType. Instances of `ContentType` represent and store information about the models installed in your project, and new instances of ContentType are automatically created whenever new models are installed.
Instances of `ContentType` have methods for returning the model classes they represent and for querying objects from those models.
Relations between your models and `ContentType` can also be used to enable “generic” relationships between an instance of one of your models and instances of any model you have installed.

The contenttypes framework is included in the default INSTALLED_APPS. several of Django’s other bundled applications require it:

The admin application uses it to log the history of each object added or changed through the admin interface.
Django’s authentication framework uses it to tie user permissions to specific models.

**`class` ContentType**

Each instance of ContentType has two fields which, taken together, uniquely describe an installed model:

  model - the nanme of the model.

  app_label - The name of the application the model is part of. This is taken from the app_label attribute of the model

Additionally, the following property is available:

  name - the human-readable name of the content type. This is taken from the verbose_name attribute of the model.

**Methods on ContentType instances**

Each ContentType instance has methods that allow you to get from a ContentType instance to the model it represents, or to retrieve objects from that model:

    ContentType.get_object_for_this_type(**kwargs)` - Takes a set of valid lookup arguments (e.g. those used with `filter()`, `exclude()` and `get()`) for the model the ContentType represents, and does a  lookup on that model, returning the corresponding object

    ContentType.model_class() - Returns the model class represented by this ContentType instance.

For example, we could look up the ContentType for the User model:

    >>> from django.contrib.contenttypes.models import ContentType
    >>> ContentType.objects.get(app_label="auth", model="user")
    <ContentType: user>
    
And then use it to query for a particular User, or to get access to the User model class:
    
    >>> user_type.model_class()
    <class 'django.contrib.auth.models.User'>
    >>> user_type.get_object_for_this_type(username='Guido')
    <User: Guido>

Together, get_object_for_this_type() and model_class() enable two extremely important use cases:

1) Using these methods, you can write high-level generic code that performs queries on any installed model – instead of importing and using a single specific model class, you can pass an app_label and model into a ContentType lookup at runtime, and then work with the model class or retrieve objects from it.

2) You can relate another model to ContentType as a way of tying instances of it to particular model classes, and use these methods to get access to those model classes.

**`class` ContentTypeManager**

ContentType uses a cache to keep track of models for which it has created ContentType instances.


    ContentType.objects.get_for_id(id)

    Lookup a ContentType by ID. Since this method uses the same shared cache as get_for_model(), it’s preferred to use this method over the usual ContentType.objects.get(pk=id)

    ContentType.objects.get_for_model(model, for_concrete_model=True)

    Takes either a model class or an instance of a model, and returns the ContentType instance representing that model. for_concrete_model=False allows fetching the ContentType of a proxy model.

The get_for_model() method is especially useful when you know you need to work with a ContentType but don’t want to go to the trouble of obtaining the model’s metadata to perform a manual lookup:

    >>> from django.contrib.auth.models import User
    >>> ContentType.objects.get_for_model(User)
    <ContentType: user>
    
 Generic relations
 ---------------
 
 
    
    
    
    
