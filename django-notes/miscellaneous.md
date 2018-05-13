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





