A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. By subclassing models.Model, you get an automatically-generated database-access API.

**Field options**

Each field takes a certain set of field-specific arguments, e.g. `CharField` require a `max_length` argument.

`null` if `True` will store empty values as `NULL` in the database. Default is `False`.

`blank` if `True`, the field is allowed to be blank. Default s `false`

Note that this is different than null. null is purely database-related, whereas `blank` is validation-related

`choices` An iterable (e.g., a list or tuple) of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given. E.g.:

    YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    )

The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.

`help_text` is for extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.

`verbose name` each field type, except for `ForeignKey`, `ManyToManyField` and `OneToOneField`, takes an optional first positional argument – a `verbose name`. If the verbose name isn’t given, Django will automatically create it
 
    first_name = models.CharField("person's first name", max_length=30) 

The relationship fields require the first argument to be a model class, so use the verbose_name keyword argument.
 
    from django.db import models
     
    class Topping(models.Model):
        # ...
        pass
     
    class Pizza(models.Model):
        # ...
        toppings = models.ManyToManyField(Topping)
 
`ManyToManyField` should only be put on one of the models. Generally, ManyToManyField instances should go in the object that’s going to be edited on a form. In the above example, toppings is in Pizza because it’s more natural to think about a pizza having toppings than vice versa. The way it’s set up above, the Pizza form would let users select the toppings.
 
Related objects can be added, removed, or created with the field’s RelatedManager.

**Extra fields on many-to-many relationships**

Consider the case of an application tracking the musical groups which musicians belong to. There is a many-to-many relationship between a person and the groups of which they are a member, so you could use a ManyToManyField to represent this relationship. However, there is a lot of detail about the membership that you might want to collect, such as the date at which the person joined the group.
 
For these situations, Django allows you to specify the model that will be used to govern the many-to-many relationship. You can then put extra fields on the intermediate model. The intermediate model is associated with the ManyToManyField using the through argument to point to the model that will act as an intermediary. 
 

        from django.db import models
         
        class Person(models.Model):
            name = models.CharField(max_length=128)
         
            def __str__(self):
                return self.name
     
        class Group(models.Model):
            name = models.CharField(max_length=128)
            members = models.ManyToManyField(Person, through='Membership')
         
            def __str__(self):
                return self.name
        
        class Membership(models.Model):
            person = models.ForeignKey(Person, on_delete=models.CASCADE)
            group = models.ForeignKey(Group, on_delete=models.CASCADE)
            date_joined = models.DateField()
            invite_reason = models.CharField(max_length=64)
 

When you set up the intermediary model, you explicitly specify foreign keys to the models that are involved in the many-to-many relationship. This explicit declaration defines how the two models are related.


ManyToManyField.through

Django will automatically generate a table to manage many-to-many relationships. However, if you want to manually specify the intermediary table, you can use the through option to specify the Django model that represents the intermediate table that you want to use.
The most common use for this option is when you want to associate extra data with a many-to-many relationship.
If you don’t specify an explicit through model, there is still an implicit through model class you can use to directly access the table created to hold the association. It has three fields to link the models.
If the source and target models differ, the following fields are generated:

    id: the primary key of the relation.
    <containing_model>_id: the id of the model that declares the ManyToManyField.
    <other_model>_id: the id of the model that the ManyToManyField points to.

If the ManyToManyField points from and to the same model, the following fields are generated:

    id: the primary key of the relation.
    from_<model>_id: the id of the instance which points at the model (i.e. the source instance).
    to_<model>_id: the id of the instance to which the relationship points (i.e. the target model instance).

This class can be used to query associated records for a given model instance like a normal model.

**Field attribute reference**

`class` Field 

An abstract class that represents a db column. A field is thus a fundamental piece in different Django APIs, notably, models and querysets.
In models, a field is instantiated as a class attribute and represents a particular table column
All of Django’s built-in fields, such as CharField, are particular implementations of Field. 

Every Field instance contains several attributes that allow introspecting its behavior. Use these attributes instead of isinstance checks when you need to write code that depends on a field’s functionality. 

These attributes can accessed with the Model._meta API

Field.is_relation 

Boolean flag that indicates if a field contains references to one or more other models

Field.model

Returns the model on which the field is defined. If a field is defined on a superclass of a model, model will refer to the superclass, not the class of the instance.

Fields with relations have relations have boolean values (other than None) for a number of attributes: 

Field.many_to_many, Fields.many_to_one, Field.related_model etc.

**Field access API**

`class` Options

The model _meta API is at the core of the Django ORM. It enables other parts of the system such as lookups, queries, forms, and the admin to understand the capabilities of each model. The API is accessible through the _meta attribute of each model class, which is an instance of an django.db.models.options.Options object.

`Options.get_field(field_name)` Returns the field instance given a name of a field.

    from django.contrib.auth.models import User
    
    # A field on the model
    >>> User._meta.get_field('username')
    <django.db.models.fields.CharField: username>
    
`Options.get_fields(include_parents=True, include_hidden=False` Returns a tuple of fields associated with a model.

*include_parents* is True by default. Recursively includes fields defined on parent classes. If set to False then only shows fields declared directly on the model. Fields from models that directly inherit from abstract models or proxy classes are considered to be local, not on the parent.

    >>> User._meta.get_fields()
    (<ManyToOneRel: admin.logentry>,
     <django.db.models.fields.AutoField: id>,
     <django.db.models.fields.CharField: password>,
     <django.db.models.fields.DateTimeField: last_login>,
     <django.db.models.fields.BooleanField: is_superuser>,
     <django.db.models.fields.CharField: username>,
     ...


