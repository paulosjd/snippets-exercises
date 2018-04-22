Model methods
Define custom methods on a model to add custom “row-level” functionality to your objects. Whereas Manager methods are intended to do “table-wide” things, model methods should act on a particular model instance.
This is a valuable technique for keeping business logic in one place – the model.

 
Proxy Models
 
Sometimes, however, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method.
This is what proxy model inheritance is for: creating a proxy for the original model. You tell Django that it’s a proxy model by setting the proxy attribute of the Meta class to True. The proxy model class still operates on the same database table as its parent.
 

**Signals**

Django includes a “signal dispatcher” which helps allow decoupled applications get notified when actions occur elsewhere in the framework. Signals allow certain senders to notify a set of receivers that some action has taken place.
Django provides a set of built-in signals that let user code get notified by Django itself of certain actions. These include:

    •  django.db.models.signals.pre_save & django.db.models.signals.post_save
    Sent before or after a model’s save() method is called.
    •  django.db.models.signals.pre_delete & django.db.models.signals.post_delete
    Sent before or after a model’s delete() method or queryset’s delete() method is called.
    •  django.db.models.signals.m2m_changed
    Sent when a ManyToManyField on a model is changed.
    •  django.core.signals.request_started & django.core.signals.request_finished
    Sent when Django starts or finishes an HTTP request.


Listening to signals

To receive a signal, register a receiver function using the `Signal.connect()` method. The receiver function is called when the signal is sent.

`Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)`

    •  receiver – The callback function which will be connected to this signal. See Receiver functions for more information.
    •  sender – Specifies a particular sender to receive signals from. See Connecting to signals sent by specific senders for more information

Let’s see how this works by registering a signal that gets called after each HTTP request is finished. We’ll be connecting to the request_finished signal.

Receiver functions:

First, we need to define a receiver function. All signal handlers must take these arguments: a sender argument, along with wildcard keyword arguments (**kwargs).

    def my_callback(sender, **kwargs):
      print("Request finished!")

Connecting receiver functions

There are two ways you can connect a receiver to a signal. You can take the manual connect route.
you can use a `receiver()` decorator:

`receiver(signal)`  Parameters:	signal – A signal or a list of signals to connect a function to.

    from django.core.signals import request_finished
    from django.dispatch import receiver

    @receiver(request_finished)
    def my_callback(sender, **kwargs):
        print("Request finished!")
    Now, our my_callback function will be called each time a request finishes.

Connecting to signals sent by specific senders

Some signals get sent many times, but you’ll only be interested in receiving a certain subset of those signals. For example, consider the django.db.models.signals.pre_save signal sent before a model gets saved. Most of the time, you don’t need to know when any model gets saved – just when one specific model is saved.
In these cases, you can register to receive signals sent only by particular senders. In the case of django.db.models.signals.pre_save, the sender will be the model class being saved, so you can indicate that you only want signals sent by some model:
Then the my_handler function will only be called when an instance of MyModel is saved.

    from django.db.models.signals import pre_save
    from django.dispatch import receiver
    from myapp.models import MyModel

    @receiver(pre_save, sender=MyModel)
    def my_handler(sender, **kwargs):
        ...


