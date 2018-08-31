API reference material for the components of Django’s authentication system:
https://docs.djangoproject.com/en/2.0/ref/contrib/auth/

The usage of Django’s authentication system in its default configuration:
https://docs.djangoproject.com/en/2.0/topics/auth/default/


The Django authentication system handles both authentication and authorization as these features are somewhat coupled. It consists of:

- Users
- Permissions: Binary (yes/no) flags designating whether a user may perform a certain task.
- Groups: A generic way of applying labels and permissions to more than one user.
- A configurable password hashing system
- Forms and view tools for logging in users, or restricting content
- A pluggable backend system

**User objects**

They typically represent the people interacting with your site. Only one class of user exists in Django’s authentication framework, i.e., 'superusers' or admin 'staff' users are just user objects with special attributes set, not different classes of user objects.
The have a number of default attributes (first_name etc.)

    >>> from django.contrib.auth.models import User
    >>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

Django does not store raw (clear text) passwords on the user model, but only a hash

A low level way to authenticate a set of credentials:

    from django.contrib.auth import authenticate
    user = authenticate(username='john', password='secret')
    if user is not None:
        # A backend authenticated the credentials
    else:
        # No backend authenticated the credentials

    request is an optional HttpRequest which is passed on the authenticate() method of the authentication backends.

Rather if you’re looking for a way to login a user, use the LoginView.

**Permissions**

The permissions systems provides a way to assign permissions to specific users and groups of users.

Permissions can be set not only per type of object, but also per specific object instance. By using the `has_add_permission()`, has_`change_permission()` and `has_delete_permission()` methods provided by the `ModelAdmin` class, it is possible to customize permissions for different object instances of the same type.

User objects have two many-to-many fields: groups and user_permissions. User objects can access their related objects in the same way as any other Django mode

Default permissions:

When `django.contrib.auth` is listed in your `INSTALLED_APPS` setting, it will ensure that three default permissions – add, change and delete – are created for each Django model defined in one of your installed applications.

Assuming you have an application with an `app_label` `foo` and a model named `Bar`, to test for basic permissions you should use:

add:

    user.has_perm('foo.add_bar')

change:

    user.has_perm('foo.change_bar')

delete:

    user.has_perm('foo.delete_bar')

The `Permission` model is rarely accessed directly.

Groups:

`django.contrib.auth.models.Group` models are a generic way of categorizing users so you can apply permissions, or some other label, to those users. A user can belong to any number of groups.

A user in a group automatically has the permissions granted to that group. For example, if the group Site editors has the permission `can_edit_home_page`, any user in that group will have that permission.

Programmatically creating permissions:

While custom permissions can be defined within a model’s `Meta` class, you can also create permissions directly. For example, you can create the `can_publish` permission for a `BlogPost` model in `myapp`:

    from myapp.models import BlogPost
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(BlogPost)
    permission = Permission.objects.create(
        codename='can_publish',
        name='Can Publish Posts',
        content_type=content_type, )








