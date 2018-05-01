Form and Field Validation
-------------------------

Form validation happens when the data is cleaned and is a process which can be customized. This is normally executed when you call the `is_valid()` method on a form.

In general, any cleaning method can raise `ValidationError` if there is a problem with the data it is processing, passing the relevant information to the ValidationError constructor.
If no `ValidationError` is raised, the method should return the cleaned (normalized) data as a Python object.

Most validation can be done using validators - simple helpers that can be reused easily. Validators are simple functions (or callables) that take a single argument and raise `ValidationError` on invalid input. Validators are run after the field’s `to_python` and `validate` methods have been called.
These two methods are run by the `clean()` method on a Field subclass, which is also responsible for propagating any errors.

The `to_python()` method on a field is the first step in validation and it coerces the value to the correct datatype, raising `ValidationError` if this is not possible. The `validate()` method on a Field handles field-specific validation that is not suitable for a validator. This method does not return anything and shouldn’t alter the value.

After the `Field.clean()` method (or its override) is run, `clean_<fieldname>()` is run. This method does any cleaning that is specific to that particular attribute, unrelated to the type of field that it is.
For example, if you wanted to validate that the contents of a `CharField` called serialnumber was unique, `clean_serialnumber()` would be the right place to do this, by looking up the value of the field in `self.cleaned_data`.

Finally, once those two methods are run for every field, the `Form.clean()` method, or its override (e.g. to add custom validation for fields that are interdependent), is executed whether or not the previous methods have raised errors.

**Using validators**

Django’s form (and model) fields support use of simple utility functions and classes known as validators. A validator is merely a callable object or function that takes a value and simply returns nothing if the value is valid or raises a `ValidationError` if not.

    class SlugField(CharField):
        default_validators = [validators.validate_slug]

    class MyForm(forms.Form):
        ...
        slug = forms.SlugField()

is equivalent to:

    class MyForm(forms.Form):
        ...
        slug = forms.CharField(validators=[validators.validate_slug])

**Built-in validators**
Common cases such as validating against an email or a regular expression can be handled using existing validator classes available in Django. For example, `validators.validate_slug` is an instance of a `RegexValidator` constructed with the first argument being the pattern: `^[-a-zA-Z0-9_]+$`.

The django.core.validators module contains a collection of callable validators for use with model and form fields. They’re used internally but are available for use with your own fields, too. They can be used in addition to, or in lieu of custom `field.clean()` methods.

**Writing custom validators**

Validators can be useful for re-using validation logic between different types of fields. Otherwise if only ever used once can put the logic in `clean_<fieldname>()` method.

    def validate_even(value):
        if value % 2 != 0:
            raise ValidationError('%(value)s is not an even number',
                params={'value': value},)

You can add this to a model field via the field’s validators argument:

    class MyModel(models.Model):
        even_field = models.IntegerField(validators=[validate_even])

Or on a form:

    class MyForm(forms.Form):
        even_field = forms.IntegerField(validators=[validate_even])

**Cleaning and validating fields that depend on each other**

Here we are talking about the `clean()` method on the form, rather than the field. By the time the form’s `clean()` method is called, all the individual field clean methods will have been run, `so self.cleaned_data` will be populated with any data that has survived so far. So you also need to remember to allow for the fact that the fields you are wanting to validate might not have survived the initial individual field checks.

    class ContactForm(forms.Form):
        ...
        def clean(self):
            cleaned_data = super().clean()
            cc_myself = cleaned_data.get("cc_myself")
            subject = cleaned_data.get("subject")

            if cc_myself and subject:
                # Only do something if both fields are valid so far.
                if "help" not in subject:
                    raise forms.ValidationError(
                        "Did not send for 'help' in the subject despite "
                        "CC'ing yourself.")

Alternatively, instead of raising `ValidationError` in the `clean()` method, could do this:

    ...
    self.add_error('cc_myself', msg)

The second argument of `add_error()` can be a simple string, or preferably an instance of `ValidationError`.
Note that `add_error()` automatically removes the field from `cleaned_data`.


