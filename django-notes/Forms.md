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

**Overriding `__init__` in ModelForms**

In instantiated Django forms, fields are kept in a dict-like object. Which means, instead of writing forms in a
way that duplicates the model, a better way is to explicitly modify only what we want to modify:

    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        self.fields['some_field'].required = True
        self.fields['some_other_field'].required = True
        self.fields['some_other_field'].widget.attrs['size'] = 40

Another example:

    class BaseEmailForm(forms.Form):
        email = forms.EmailField("Email")
        email2 = forms.EmailField("Email 2")

        def clean(self, *args, **kwargs):
            email = self.cleaned_data['email']
            email2 = self.cleaned_data['email2']
            if email != email2:
                raise forms.ValidationError("Emails don't match")
            return self.cleaned_data

    class ContactForm(BaseEmailForm):
        message = forms.CharField()

        def __init__(self, *args, **kwargs):
            super(ContactForm, self).__init__(*args, **kwargs):
            self.fields['email2'].label = "Confirm your email"
            self.fields['email2'].help_text = "We want to be sure!"


**Inheritance**

It is possible to inherit from both Form and ModelForm, but you must ensure ModelForm
appears first in the MRO. This is because the classes rely on different metaclasses and a
class can only have one metaclass.


**Hidden Fields**

    # forms.py
    class SomeForm(forms.Form):
        hidden = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

    template.html
    {% for hidden in form.hidden_fields %}
        {{ hidden }}
    {% endfor %}


Stackoverflow  Q's on `form.save()`
-----------------------------------

**Q: How to override `form.save()`?**

My model has quite a few boolean fields. I've broken these up into 3 sets which I'm rendering as a `MultipleChoiceField` w/ a modified `CheckboxSelectMultiple`.

Now I need to save this data back to the DB. i.e., I need to split the data returned by a single widget into multiple boolean columns. I think this is appropriate for the `save()` method, no?

Question is, how do I do I do it? Something like this?

    def save(self, commit=True):
        # code here
        return super(MyForm, self).save(commit)

If so... how do I set the values? `self.fields['my_field'].value = 'my_flag' in self.cleaned_data['multi_choice']` Or something? Where's all the data stored?

**Answer**

The place you want your data to be stored is your new model instance:

    def save(self, commit=True):
        instance = super(MyForm, self).save(commit=False)
        instance.flag1 = 'flag1' in self.cleaned_data['multi_choice'] # etc
        if commit:
            instance.save()
        return instance


**Q: Overriding the save method in Django ModelForm**

I'm having trouble overriding a ModelForm save method. This is the error I'm receiving:

    Exception Type:     TypeError
    Exception Value:    save() got an unexpected keyword argument 'commit'

My intentions are to have a form submit many values for 3 fields, to then create an object for each combination of those fields, and to save each of those objects. Helpful nudge in the right direction would be ace.

    #File models.py

    class CallResultType(models.Model):
        id = models.AutoField(db_column='icontact_result_code_type_id', primary_key=True)
        callResult = models.ForeignKey('CallResult', db_column='icontact_result_code_id')
        campaign = models.ForeignKey('Campaign', db_column='icampaign_id')
        callType = models.ForeignKey('CallType', db_column='icall_type_id')
        agent = models.BooleanField(db_column='bagent', default=True)
        teamLeader = models.BooleanField(db_column='bTeamLeader', default=True)
        active = models.BooleanField(db_column='bactive', default=True)

    #File forms.py

    from django.forms import ModelForm, ModelMultipleChoiceField
    from callresults.models import *

    class CallResultTypeForm(ModelForm):
        callResult = ModelMultipleChoiceField(queryset=CallResult.objects.all())
        campaign = ModelMultipleChoiceField(queryset=Campaign.objects.all())
        callType = ModelMultipleChoiceField(queryset=CallType.objects.all())

        def save(self, force_insert=False, force_update=False):
            for cr in self.callResult:
                for c in self.campain:
                    for ct in self.callType:
                        m = CallResultType(self) # this line is probably wrong
                        m.callResult = cr
                        m.campaign = c
                        m.calltype = ct
                        m.save()

        class Meta:
            model = CallResultType

    #File admin.py

    class CallResultTypeAdmin(admin.ModelAdmin):
        form = CallResultTypeForm

**Answer**

In your save you have to have the argument commit. If anything overrides your form, or wants to modify what it's saving, it will do `save(commit=False)`, modify the output, and then save it itself.

Also, your ModelForm should return the model it's saving. Usually a ModelForm's save will look something like:

    def save(self, commit=True):
        m = super(CallResultTypeForm, self).save(commit=False)
        # do custom stuff
        if commit:
            m.save()
        return m

Finally, a lot of this ModelForm won't work just because of the way you are accessing things. Instead of `self.callResult`, you need to use self.fields['callResult'].
Aside: Why not just use ManyToManyFields in the Model so you don't have to do this? Seems like you're storing redundant data and making more work for yourself (and me :P).

    from django.db.models import AutoField
    def copy_model_instance(obj):
        """
        Create a copy of a model instance.
        M2M relationships are currently not handled, i.e. they are not copied. (Fortunately, you don't have any in this case)
        See also Django #4027. From http://blog.elsdoerfer.name/2008/09/09/making-a-copy-of-a-model-instance/
        """
        initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])
        return obj.__class__(**initial)

    class CallResultTypeForm(ModelForm):
        callResult = ModelMultipleChoiceField(queryset=CallResult.objects.all())
        campaign = ModelMultipleChoiceField(queryset=Campaign.objects.all())
        callType = ModelMultipleChoiceField(queryset=CallType.objects.all())

        def save(self, commit=True, *args, **kwargs):
            m = super(CallResultTypeForm, self).save(commit=False, *args, **kwargs)
            results = []
            for cr in self.callResult:
                for c in self.campain:
                    for ct in self.callType:
                        m_new = copy_model_instance(m)
                        m_new.callResult = cr
                        m_new.campaign = c
                        m_new.calltype = ct
                        if commit:
                            m_new.save()
                        results.append(m_new)
             return results

This allows for inheritance of CallResultTypeForm, just in case that's ever necessary.

