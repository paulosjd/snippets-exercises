D-R-F 

Good url routing essential to make API RESTful.
DRF helps 

The validation to ensure data format so can have a good consistent representation of your resources (your models) in say your json. Validation defined in serializer class, which very similar to forms class.

The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the snippet instances into representations such as json. We can do this by declaring serializers that work very similar to Django's forms. 

**`class ViewSet`**

A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as `get()` or `post()`, and instead provides actions such as `list()` and `create()`.
The method handlers for a `ViewSet` are only bound to the corresponding actions at the point of finalizing the view, using the `as_view()` method.
Typically, rather than explicitly registering the views in a viewset in the urlconf, you'll register the viewset with a router class, that automatically determines the `URLconf` for you.
REST framework includes an abstraction for dealing with `ViewSets`, that allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.
`ViewSet` classes are almost the same thing as `View` classes, except that they provide operations such as read, or update, and not method handlers such as get or put.
A `ViewSet` class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a `Router` class which handles the complexities of defining the `URLconf` for you.
`ViewSets` and `Routers` are very useful for slimming up your code and providing a lot of default functionality out of the box. They are powerful features in django-rest-framework allowing a lot of flexibility in your code while keeping things clean. 