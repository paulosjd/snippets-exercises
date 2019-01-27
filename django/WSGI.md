WSGI
------

**Web Server**

Web servers serve up responses. They wait until the receive a request from a client, various things happen (e.g. software runs), then the send back a response to the client. They are very good at this: they scale up and down processing depending on demand, they reliably hold conversations with the flakiest of clients. They know nothing about content, nothing about users, nothing in fact other than how to wait a lot and reply reliably. Your web server should be in charge of serving, not processing or logical stuff. A traditional web server does not understand or have any way to run Python applications.

**(Python) Software**

Conversely, software does not sit around and wait. It only exists at exists at runtime. Software is not terribly accommodating when it comes to unexpected changes in its environment so code is put in the application to cope with the physical server environment or, at least, being forced to choose an appropriate 'wrapper' library to include at runtime, to give the illusion of uniformity across web servers.

**WSGI**

A specification that describes how a web server communicates with web applications, and how web applications can be chained together to process one request It is just an interface specification by which server and application communicate - WSGI provides the common ground for Python web application development because it provides a universal, standardised low-level interface between web servers and web frameworks.

Both server and application interface sides are specified in the PEP 3333. If an application/framework is written to the WSGI spec then it will run on any server written to that spec. You generally do not need to know about WSGI if using a framework which supports WSGI.  You only need to worry about configuration and deployment of your app.

WSGI is a set of rules, written in two halves: The first part, written for the web server side, defines how the software will be thinking when it loads, the things you must make available to the application, and how the app can be expected to behave if anything goes wrong. The second part, written for the Python application defines how the server will be thinking when it contacts it, the things you must make available to the server, and the interface that you expect the server to have, and how to handle errors.

So there you have it - servers will be servers and software will be software, and here's a way they can get along just great without one having to make any allowances for the specifics of the other. This is WSGI.

mod_ is a plugin for Apache that lets it talk to WSGI-compliant software, so mod_wsgi is an implementation - in Apache - of the rules of part one of the rulebook above. It is easy to switch from one wsgi compliant web server, i.e gunicorn, to another wsgi compliant web server, i.e uWSGI. WSGI runs the Python interpreter on web server, either as part of the web server process (embedded mode) or as a separate process (daemon mode), and loads the script into it. Each request results in a specific function in the script being called, with the request environment passed as arguments to the function.

There are two major sides to the WSGI framework:

a. WSGI Application/Framework made from Python script

b. WSGI Server/Gateway like Apache or Nginx

Being a callable object, WSGI paces two arguments through a __call__ method, according to PEP 333. They are:

1. WSGI environment as first argument

2. Function that starts the response

There are two major sides to the WSGI framework:

a. WSGI Application/Framework made from Python script

b. WSGI Server/Gateway like Apache or Nginx

Being a callable object, WSGI paces two arguments through a __call__ method, according to PEP 333. They are:

1. WSGI environment as first argument

2. Function that starts the response

Each time it receives a request from the HTTP clients directed towards the application, an application callable is invoked by the server/gateway. Eventually WSGI became the accepted approach for running Python applications. It is the server that triggers the web app, and transmits related information, with callback function to the app. The processing of the request takes place on the app side, while the server receives the response, by making use of the callback function. There could be more than one WSGI middleware between the web app and the server. Their function would be to direct requests to various app objects, content preprocessing, load balancing and so on. WSGI middleware complies with both sides of the WSGI specification.

Application Configuration
-------------------------

Django contains a registry of installed applications that stores configuration and provides introspection. It also maintains a list of available models.

This registry is simply called apps and it’s available in `django.apps`:

    >>> from django.apps import apps
    >>> apps.get_app_config('admin').verbose_name
    'Admin'

The project Python package is defined primarily by a settings module. The term application describes a Python package that provides some set of features. Applications may be reused in various projects.

Applications are generally wired into projects with the `INSTALLED_APPS` setting and optionally with other mechanisms such as `URLconfs`.
`INSTALLED_APPS` should contain a dotted path to the appropriate AppConfig subclass.

There’s no such thing as an Application object.  That’s why the application registry maintains metadata in an `AppConfig` instance for each installed application.

If you’re creating a pluggable app called “Rock ’n’ roll”, here’s how you would provide a proper name for the admin:

    # rock_n_roll/apps.py
    from django.apps import AppConfig

    class RockNRollConfig(AppConfig):
        name = 'rock_n_roll'
        verbose_name = "Rock ’n’ roll"

You must include the name attribute for Django to determine which application this configuration applies to. You can define any attributes documented in the AppConfig API reference.


`class AppConfig` Application configuration objects store metadata for an application. Some attributes can be configured in AppConfig subclasses. Others are set by Django and read-only.

`AppConfig.name`  Full Python path to the application, e.g. 'django.contrib.admin'. It must be unique across a Django project.

`AppConfig.verbose_name` Human-readable name for the application, e.g. “Administration”.

`AppConfig.get_models()` Returns an iterable of Model classes for this application.

`AppConfig.get_model(model_name, require_ready=True)` Returns the Model with the given model_name. model_name is case-insensitive.

`AppConfig.ready()`

Subclasses can override this method to perform initialization tasks such as registering signals. It is called as soon as the registry is fully populated.

If you’re registering model signals, you can refer to the sender by its string label instead of using the model class itself. Example:

    from django.db.models.signals import pre_save

    def ready(self):
        # importing model classes
        from .models import MyModel  # or...
        MyModel = self.get_model('MyModel')

        # registering signals with the model's string label
        pre_save.connect(receiver, sender='app_label.MyModel')

The application registry provides a public API. e.g. `apps.is_installed(model_name`, `apps.get_model(app_label, model_name, require_ready=True)`

**Middleware**

Lightweight “plug-ins” for Django that alter the input and output. Django comes with built-in middleware components, classes defined in settings, and are called during both request and response cycle. During the request cycle, the Middleware classes are executed top-down, meaning it will first execute SecurityMiddleware, then SessionMiddleware . For each of the Middlewares it will execute the `process_request()` and `process_view()` methods.
After Django has process the views the response cycle begins and the middleware is executed in reverse order which is when methods such as `process_exception()`, and `process_response()` methods are executed.



