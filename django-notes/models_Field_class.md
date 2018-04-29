    class Hand:
        """A hand of cards (bridge style)"""

        def __init__(self, north, east, south, west):
            # Input parameters are lists of cards ('Ah', '9s', etc.)
            self.north = north
            self.east = east
            self.south = south
            self.west = west

Field is an abstract class that represents a database table column. Django uses fields to create the database table (`db_type()`), to map Python types to database (`get_prep_value(`)) and vice-versa (`from_db_value()`).

Background theory
-----------------
The simplest way to think of a model field is that it provides a way to take a normal Python
object – string, boolean, datetime, or something more complex like a class, and convert it to and
from a format that is useful when dealing with the database (and serialization).

Different databases provide different sets of valid column types. Anything you want to store in the database must fit into one of those types.
Normally, with a CharField for instance, storing a string is straigtforward.
or our Hand example, we could convert the card data to a string of 104 characters by concatenating
all the cards together in a pre-determined order – say, all the north cards first, then the east and so on.
So Hand objects can be saved to text or character columns in the database.

**What does a field class do?**
All of Django's models fields are subclasses of django.db.models.Field.
Storing information common to all fields (name, help text, uniqueness etc.) is handled by Field.

When a model is created, the field classes you define in a model are actually stored in the model's Meta class.
This is because the field classes aren’t necessary when you’re just creating and modifying attributes. Instead, they provide the machinery for converting between the attribute value and what is stored in the database or sent to the serializer.

Creating custom model fields
--------------------------

For more obscure column types, such as geographic polygons, you can define your own Django Field subclasses.
Alternatively, you may have a complex Python object that can somehow be serialized to fit into a standard database column type. This is another case where a Field subclass will help you use your object with your models.


We would like to be able to do things like this:

    example = MyModel.objects.get(pk=1)
    print(example.hand.north)

    new_hand = Hand(north, east, south, west)
    example.hand = new_hand
    example.save()

The trick is to tell Django how to handle saving and loading such an object.
When planning your Field subclass, first give some thought to which existing Field class your new field is most similar to. Can you subclass an existing Django field and save yourself some work? If not, you should subclass the Field class, from which everything is descended.

Initializing your new field is a matter of separating out any arguments that are specific to your case from the common arguments and passing the latter to the __init__() method of Field (or your parent class).

    class HandField(models.Field):

        description = "A hand of cards (bridge style)"

        def __init__(self, *args, **kwargs):
            kwargs['max_length'] = 104
            super().__init__(*args, **kwargs)

The `Field.__init__()` method takes the parameters such as verbose_name, db_index, max_length, primary_key etc. and have the same meaning they do for normal Django fields.

**Field deconstruction**

This method tells Django how to take an instance of your new field and reduce it to a serialized form - in particular, what arguments to pass to `__init__()` to re-create it.
If you’re changing the arguments passed in `__init__()` (like in HandField), you’ll need to supplement the values being passed by writing a `deconstruct()` method.

The method returns a tuple of four items: the field’s attribute name, the full import path of the field class, the positional arguments (as a list), and the keyword arguments (as a dict).
The base Field class has all the code to work out the field’s attribute name and import path. You do, however, have to care about the positional and keyword arguments, as these are likely the things you are changing.

For example, in our HandField class we’re always forcibly setting max_length in __init__(). The deconstruct() method on the base Field class will see this and try to return it in the keyword arguments; thus, we can drop it from the keyword arguments for readability:

    class HandField(models.Field):

        def __init__(self, *args, **kwargs):
            kwargs['max_length'] = 104
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            del kwargs["max_length"]
            return name, path, args, kwargs

If you add a new keyword argument, you need to write code to put its value into kwargs yourself:

    class CommaSepField(models.Field):
        "Implements comma-separated storage of lists"

        def __init__(self, separator=",", *args, **kwargs):
            self.separator = separator
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            # Only include kwarg if it's not the default
            if self.separator != ",":
                kwargs['separator'] = self.separator
            return name, path, args, kwargs

If your custom Field class deals with data structures that are more complex than strings, dates, integers, or floats, then you may need to override `from_db_value()` and `to_python()`.
`to_python()` is called by deserialization and during the `clean()` method used from forms.

If present for the field subclass, `from_db_value()` will be called in all circumstances when the data is loaded from the database.

Since using a database requires conversion in both ways, if you override `to_python()` you also have to override `get_prep_value()` to convert Python objects back to query values.





