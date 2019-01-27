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

**`class` Media**

Rendering attractive forms requires CSS and JavaScript as well as HTML.
Asset definitions allows .js and .css files to be associated with the forms
 and widgets that require them.

This is done by declaring an inner Media class:

    class CalendarWidget(forms.TextInput):
        class Media:
            css = {
                'all': ('pretty.css',)
            }
            js = ('animations.js', 'actions.js')

 Every time the CalendarWidget is used on a form, that form will be directed to include the CSS file pretty.css, and the JavaScript files animations.js and actions.js.
 This static definition is converted at runtime into a widget property named media.
 The keys in the css dictionary are the output media types,  If you need to have different stylesheets for different media types, provide a list of CSS files for each output medium, e.g:

    class Media:
        css = {
            'screen': ('pretty.css',),
            'print': ('newspaper.css',)
        }

**Media on Forms**

Widgets aren’t the only objects that can have media definitions – forms can also define media

When you interrogate the media attribute of a widget or form, the value that is returned is a forms.Media object. As we have already seen, the string representation of a Media object is the HTML required to include the relevant files in the \<head> block of your HTML page.

    >>> w = CalendarWidget()
    >>> print(w.media)
    <link href="http://static.example.com/pretty.css" type="text/css" media="all" rel="stylesheet" />
    <script type="text/javascript" src="http://static.example.com/animations.js"></script>
    <script type="text/javascript" src="http://static.example.com/actions.js"></script>

    >>> print(w.media['css'])
    <link href="http://static.example.com/pretty.css" type="text/css" media="all" rel="stylesheet" />