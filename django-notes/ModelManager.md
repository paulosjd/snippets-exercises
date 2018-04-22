`class Manager`
---------------


Django has two intimately-related constructs related to table-level operations: managers and querysets.

A manager is the interface through which database query operations (see Queryset API) are provided to Django models. By default, Django adds a Manager with the name objects to every Django model class.

A queryset is essentially a lazily-evaluated abstraction of the result of a SELECT query, and can be filtered, ordered and generally manipulated

Using Django's low-level ORM query methods (filter, order_by etc.) directly in a view is often considered to be not ideal. It is usually preferable to build query APIs at the the model layer, where our business logic belongs.

For instance, you may have two views (e.g. a generic ListView and a ListAPIView)
which perform the same query, which would go against the DRY principle and cause more work to maintain these views.

Custom Managers
---------------
There are two reasons you might want to customize a Manager:

    1) to add extra Manager methods (e.g. complex and reusable filters)
    2) and/or to modify the initial QuerySet the Manager returns.

**Add extra methods**

    class PollManager(models.Manager):
        def with_counts(self):
            # return e.g. some complex aggregate query

    class OpinionPoll(models.Model):
        question = models.CharField(max_length=200)
        poll_date = models.DateField()
        objects = PollManager()

Note that the `get_queryset method` has not been overridden.

    OpinionPoll.objects.with_counts()
    OpinionPoll.objects.filter(...)

**Modify the initial queryset**

You can override a Manager’s base QuerySet by overriding the `Manager.get_queryset()` method.

    class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author='Roald Dahl')

    class Book(models.Model):
        title = models.CharField(max_length=100)
        author = models.CharField(max_length=50)

    objects = models.Manager() # The default manager.
    dahl_objects = DahlBookManager() # The Dahl-specific manager.

Because `get_queryset()` returns a QuerySet object, you can use `filter()`, `exclude()` and all the other QuerySet methods on it. So these statements are all legal:

    Book.dahl_objects.all()
    Book.dahl_objects.filter(title='Matilda')
    Book.dahl_objects.count()

You can attach as many `Manager()` instances to a model as you’d like. This is an easy way to define common “filters” for your models.

Calling custom QuerySet methods from the manager
-------------------------------------------------

While most methods from the standard QuerySet are accessible directly from the Manager, this is only the case for the extra methods defined on a custom QuerySet if you also implement them on the Manager:

    class DocumentQuerySet(models.QuerySet):
        def pdfs(self):
            return self.filter(file_type='pdf')

        def smaller_than(self, size):
            return self.filter(size__lt=size)

    class DocumentManager(models.Manager):
        def get_queryset(self):
            return DocumentQuerySet(self.model, using=self._db)

        def pdfs(self):
            return self.get_queryset().pdfs()

        def smaller_than(self, size):
            return self.get_queryset().smaller_than(size)

    class Document(models.Model):
        name = models.CharField(max_length=30)
        size = models.PositiveIntegerField(default=0)
        file_type = models.CharField(max_length=10, blank=True)

    objects = DocumentManager()

Now you can use it just like any other QuerySet method:

    Document.objects.pdfs().smaller_than(1000).exclude(name='Article').order_by('name')

If you are only defining custom QuerySets in the Manager, you can simply extend the models.QuerySet and in the model set the manager using the `as_manager()` method:

    class DocumentQuerySet(models.QuerySet):
        def pdfs(self):
            return self.filter(file_type='pdf')

        def smaller_than(self, size):
            return self.filter(size__lt=size)

    class Document(models.Model):
        name = models.CharField(max_length=30)
        size = models.PositiveIntegerField(default=0)
        file_type = models.CharField(max_length=10, blank=True)

    objects = DocumentQuerySet.as_manager()

 Manager Inheritance
----------------------------

All managers are inherited and if there are no managers defined in ethier parent or child class the default manager is available.

If we aren’t using a custom manager in the child class, the default manager (‘default_manager_name’ defined in the class Meta, or the manager first defined) will be inherited following the inheritance rules of python.

If you want to inherit from the AbstractBase model below, which has a manager, but provide another manager:

    class AbstractBase(models.Model):
        # ...
        objects = CustomManager()

        class Meta:
            abstract = True

    class ChildA(AbstractBase):
        # ...
        # This class has CustomManager as the default manager.
        pass

    class ChildB(AbstractBase):
        # ...
        # An explicit default manager.
        default_manager = OtherManager()

Here, default_manager is the default. The objects manager is still available, since it’s inherited. It just isn’t used as the default.

Related Objects Reference
--------------------------

**`class` RelatedManager**

A “related manager” is a manager used in a one-to-many or many-to-many related context. This happens in two cases:
The “other side” of a ForeignKey relation. That is:
from django.db import models

    class Reporter(models.Model):
        # ...
        pass

    class Article(models.Model):
        reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    
Both sides of a ManyToManyField relation:

    class Topping(models.Model):
        # ...
        pass

    class Pizza(models.Model):
        toppings = models.ManyToManyField(Topping)

In this example, the methods below will be available both on topping.pizza_set and on pizza.toppings.

Methods are available to add to, remove from, clear and replace a related object set.  
   
    b = Blog.objects.get(id=1)
    e = Entry.objects.get(id=234)
    b.entry_set.add(e) # Associates Entry e with Blog b.
  
**related_name**

The related_name attribute in the ForeignKey fields is extremely useful. Default if undefined is e.g. entry_set ? It let’s us define a meaningful name for the reverse relationship.

    class Company:
        name = models.CharField(max_length=30)

    class Employee:
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
        company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

That means the Company model will have a special attribute named employees, which will return a QuerySet with all employees instances related to the company.

    google = Company.objects.get(name='Google')
    google.employees.all()

You can also use the reverse relationship to modify the company field on the Employee instances:

    vitor = Employee.objects.get(first_name='Vitor')
    google = Company.objects.get(name='Google')
    google.employees.add(vitor)


