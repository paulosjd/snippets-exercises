Model methods
Define custom methods on a model to add custom “row-level” functionality to your objects. Whereas Manager methods are intended to do “table-wide” things, model methods should act on a particular model instance.
This is a valuable technique for keeping business logic in one place – the model.

 
Proxy Models
 
Sometimes, however, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method.
This is what proxy model inheritance is for: creating a proxy for the original model. You tell Django that it’s a proxy model by setting the proxy attribute of the Meta class to True. The proxy model class still operates on the same database table as its parent.
 