A save on a model instance triggers the following steps:

    Emit a pre-save signal.
    ...
    Insert the data into the database.
    Emit a post-save signal.

The connection between the senders (e.g. a model emitting a `post_save` signal) and the receivers (a function or method within e.g. a signals.py file) is done through “signal dispatchers”, which are instances of `Signal`, via the `connect` method.

    from django.contrib.auth.models import User
    from django.db.models.signals import post_save

    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(save_profile, sender=User)

Here, `save_profile` is the *receiver* function, `User` is the *sender* and `post_save` is the *signal*. The `save_profile` function should be run every time a User model is saved.

The `post_save` built-in signal lives in the `django.db.models.signals` module. This particular signal fires right after a model finish executing its `save` method.

Another way to register a signal, is by using the `@receiver` decorator:

    from django.dispatch import receiver

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

Here the `save_profile` function is registered to receive the `post_save` signal from the User model.

`pre-save` my be used as follows, instead of setting up a slug value from the title in the `save()` method override e.g.:

    class TodoList(models.Model):
    title = models.CharField(maxlength=100)
    slug = models.SlugField(maxlength=100)
    def save(self):
        self.slug = title
        super(TodoList, self).save()

Could use `pre-save` signal instead (n.b. in this case it would be simpler to leave it in the save method).

    from django.template.defaultfilters import slugify

    @receiver(pre_save)
    def my_callback(sender, instance, *args, **kwargs):
        instance.slug = slugify(instance.title)

Note: if you don't include the sender argument in the decorator, like `@receiver(pre_save, sender=MyModel)`, the callback will be called for all models.

A common use case of the post_save signal is UserProfile object creation, when a User object is created in the system.
You can register a post_save signal which creates a UserProfile object that corresponds to every User in the system.
Signals are a way to keep things modular, and explicit. (Explicitly notify ModelA if i save or change something in ModelB )

**Django docs - Signals**

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


