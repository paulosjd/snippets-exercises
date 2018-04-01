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
  
