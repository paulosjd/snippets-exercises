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


 
 