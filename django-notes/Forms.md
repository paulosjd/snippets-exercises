Some form interface elements - text input or checkboxes - are fairly simple and are built into HTML itself. Others are much more complex; such as an interface that pops up a date picker and will typically use JS and CSS as well as HTML form \<input>.
As an example, the login form for the Django admin contains several \<input> elements: one of type="text" for the username, one of type="password" for the password, and one of type="submit" for the “Log in” button. It also contains some hidden text fields that the user doesn’t see, which Django uses to determine what to do next.
It also tells the browser that the form data should be sent to the URL specified in the \<form>’s action attribute - /admin/ - and that it should be sent using the HTTP mechanism specified by the method attribute - post.
When the \<input type="submit" value="Log in"> element is triggered, the data is returned to /admin/.

Django handles much of the work involved in forms such as creating HTML forms for the data as well as receiving and processing submitted forms and data from the client

**The Django Form class**

Describes a form and determines how it works and appears. In a similar way that a model class’s fields map to database fields, a form class’s fields map to HTML form \<input> elements. (A ModelForm maps a model class’s fields to HTML form \<input> elements via a Form.

A form’s fields are themselves classes; they manage form data and perform validation when a form is submitted. A DateField and a FileField handle very different kinds of data and have to do different things with it.
A form field is represented to a user in the browser as an HTML “widget” - a piece of user interface machinery. Each field type has an appropriate default Widget class, but these can be overridden as required.

When we handle a model instance in a view, we typically retrieve it from the database. When we’re dealing with a form we typically instantiate it in the view.
A Form instance has an `is_valid()` method, which runs validation routines for all its fields (such as maxlength for a TextField). When this method is called, if all fields contain valid data, it will:
return True and place the form’s data in its cleaned_data attribute. 

**The view and template**

Form data sent back to a Django website is processed by a view. After instantiated the form in the view, we don't need to do much in the template, the simplest example is:

    <form action="/your-name/" method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit" value="Submit" />
    </form>

The distinction between Bound and unbound forms is important:

    An unbound form has no data associated with it. When rendered to the user, it will be empty or will contain default values.
    A bound form has submitted data, and hence can be used to tell if that data is valid. If an invalid bound form is rendered, it can include inline error messages telling the user what data to correct.
    The form’s is_bound attribute will tell you whether a form has data bound to it or not.
    
**Form rendering options**

There are other output options though for the \<label>/\<input> pairs:

    {{ form.as_table }} will render them as table cells wrapped in <tr> tags
    {{ form.as_p }} will render them wrapped in <p> tags
    {{ form.as_ul }} will render them wrapped in <li> tags

Note that, as with this \<form> tag, you’ll have to provide the surrounding \<table> or \<ul> elements yourself.

**The Forms API**

To create an unbound Form instance, simply instantiate the class:

    >>> f = ContactForm()

o bind data to a form, pass the data as a dictionary as the first parameter to your Form class constructor:

    >>> data = {'subject': 'hello',
    ...         'message': 'Hi there',
    ...         'sender': 'foo@example.com',
    ...         'cc_myself': True}
    >>> f = ContactForm(data)
    
` Form.clean()`

Implemented when you must add custom validation for fields that are interdependent

` Form.is_valid()`

With a bound Form instance, call the is_valid() method to run validation and return a boolean designating whether the data was valid:

    >>> f = ContactForm(data)
    >>> f.is_valid()
    True
    
` Form.errors`

Suppose the form data had errors:

    >>> f.errors
    {'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
    
You can access errors without having to call is_valid() first. The form’s data will be validated the first time either you call is_valid() or access errors

**Form.initial**

    >>> f = ContactForm(initial={'subject': 'Hi there!'})
 
**Form.cleaned_data**

Each field in a Form class is responsible not only for validating data, but also for “cleaning” it – normalizing it to a consistent format.
For example, DateField normalizes input into a Python datetime.date object.

If your data does *not* validate, the cleaned_data dictionary contains only the valid fields:

    >>> data = {'subject': '',
    ...         'message': 'Hi there',
    ...         'sender': 'invalid email address',
    ...         'cc_myself': True}
    >>> f = ContactForm(data)
    >>> f.is_valid()
    False
    >>> f.cleaned_data
    {'cc_myself': True, 'message': 'Hi there'}    

**Subclassing forms**

If you have multiple Form classes that share fields, you can use subclassing to remove redundancy.

    class ContactFormWithPriority(ContactForm):
        priority = forms.CharField()

    class PersonForm(forms.Form):
        first_name = forms.CharField()
        last_name = forms.CharField()
    class InstrumentForm(forms.Form):
        instrument = forms.CharField()
    class BeatleForm(InstrumentForm, PersonForm):
        haircut_type = forms.CharField()

**Widgets**

A widget is Django’s representation of an HTML input element.
Each form field has a corresponding Widget class, which in turn corresponds to an HTML form widget such as \<input type="text">.
In most cases, the field will have a sensible default widget. E.g. a CharField will have a TextInput widget, that produces an \<input type="text"> in the HTML, but say you could use \<textarea> instead
The widget handles the rendering of the HTML, and the extraction of data from a GET/POST dictionary that corresponds to the widget.

`class Widget(attrs=None)` This abstract class cannot be rendered, but provides the basic attribute attrs. 

A dictionary containing HTML attributes to be set on the rendered widget.

    >>> name = forms.TextInput(attrs={'size': 10, 'title': 'Your name'})
    >>> name.render('name', 'A name')
    '<input title="Your name" type="text" name="name" value="A name" size="10" />'
 
If you want to use a different widget for a field to the default, you can just use the widget argument on the field definition. For example:
 
    class CommentForm(forms.Form):
        name = forms.CharField()
        url = forms.URLField()
        comment = forms.CharField(widget=forms.Textarea)
    
This would specify a form with a comment that uses a larger Textarea widget, rather than the default TextInput widget. Many widgets have optional extra arguments. The following DateFields would provide a widget allow a selection from a sequence:
 
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
 
You might want a larger input element for the comment, or the ‘name’ widget to have a special CSS class. Also is possible to specify the ‘type’ attribute to take advantage of new HTML5 input types via the Widget.attrs argument when creating the widget:
 
name.widget.attrs.update({'class': 'special'})
comment.widget.attrs.update(size='40')
 
Or if the field isn’t declared directly on the form (such as model form fields), you can use the Form.fields attribute:
    
    class CommentForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].widget.attrs.update({'class': 'special'})
            self.fields['comment'].widget.attrs.update(size='40')

**Inheritance**

It is possible to inherit from both Form and ModelForm, but you must ensure ModeflFOrm
appears first in the MRO. This is because the classes rely on different metaclasses and a
class can only have one metaclass.




