A template contains the static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted.

Django defines a standard API for loading and rendering templates regardless of the backend. Loading consists of finding the template for a given identifier and preprocessing it, usually compiling it to an in-memory representation. Rendering means interpolating the template with context data and returning the resulting string.
 
The template system is meant to express presentation, not program logic.A template is simply a text file. It can generate any text-based format (HTML, XML, CSV, etc.).
A template contains *variables*, which get replaced with values when the template is evaluated, and *tags*, which control the logic of the template. E.g.:

    {% extends "base_generic.html" %}
    {% block title %}{{ section.title }}{% endblock %}
    {% block content %}
    <h1>{{ section.title }}</h1>
    {% for story in story_list %}
    <h2>
      <a href="{{ story.get_absolute_url }}">
        {{ story.headline|upper }}
      </a>
    </h2>
    <p>{{ story.tease|truncatewords:"100" }}</p>
    {% endfor %}
    {% endblock %}

When the template engine encounters a variable it tries the following lookups, in this order:

Dictionary lookup > Attribute or method lookup > Numeric index lookup.

If the resulting value is callable, it is called with no arguments. E.g.:

    {% for k, v in mydict.items %}
        Do something with k and v here...
    {% endfor %}

**General good practice**

Keep templates in one place. The convention is to make a subdirectory for each Django app, with subdirectories within those subdirectories as needed.  Storing all templates in the root level of a single directory gets messy. To load a template that’s within a subdirectory, just use a slash, like so:
`get_template('news/story_detail.html')`

Think PEP8 conventions: consistent spacing etc.
Use `{# this won't be rendered #}` rather than `<!-- this -->`. End your block structures: `{% endblock title %}` instead of: `{% endblock %}`

When including templates, try not to include in an include as it gets confusing.
Common block tags which are useful: title, extra_head (CSS, etc.), content, extra_js (so that JavaScript can go at bottom of page).
 
Name `{% url %}` tags as much as possible, define URL patterns in urls.py

    url(r'^foo/$', foo, name="foo"),
    <a href="{% url "foo" %}">foo</a>

    {{ STATIC_URL }}css/style.css
    {# Not /static/css/style.css #}

There are multiple ways to accomplish the same task, no ultimately right or wrong way. E.g:

    {% if foo.bar %}
        {{ foo.bar }}
    {% else %}
        {{ foo.baz }}
    {% endif %}

or the shorter way:

    {% firstof foo.bar foo.baz %}

**Custom Tags and Filters**

    from django import template
    register = template.Library()

    @register.filter(name='remove')

    def cut(value, argument):
        #remove passed arguments from value
        return value.replace(argument, '')

    {{ foo|remove:'bar' }}

Given that we have template tags in `demo/templatetags/demo_utils.py`
`{% load demo_utils %}`
 
**HTML Escaping**

HTML escaping is on by default in Django templates, to avoid risk of HTML injection. The escape filter makes replacements e.g. `<` is converted to `&lt;`
If you add the template filter `safe` like `{{c.title|safe}}` then the string is marked as such and it means that it won't be escaped (ensure the data is sanitized).

**Using the template system in Python**

Essentially is a three-step process:

    1. You configure an Engine.
    2. You compile template code into a Template.
    3. You render the template with a Context.

First Django instantiates an Engine. DjangoTemplates wraps Engine and adapts it to the common template backend API.
The django.template.loader module provides functions such as get_template() for loading templates.
The Template obtained in the previous step has a render() method which marshals a context and possibly a request into a Context and delegates the rendering to the underlying Template.

**Configuring an Engine**

`class Engine(debug=False, context_processors=None, autoescape=True...)`

`Engine.from_string(template_code)`  Compiles the given template code and returns a Template object.

`Engine.get_template(template_name)` Loads a template with the given name, compiles it and returns a Template object.

`Engine.select_template(template_name_list)`  Like `get_template()`, except it takes a list of names and returns the first template that was found.

**Loading a template**

The recommended way to create a Template is by calling the factory methods of the Engine: `get_template()`, `select_template()` and `from_string()`.

In a Django project where the TEMPLATES setting defines a DjangoTemplates engine, it’s possible to instantiate a Template directly:

    from django.template import Template

    template = Template("My name is {{ my_name }}.")

**Rendering a context**

Once you have a compiled `Template` object, you can render a context with it. You can reuse the same template to render it several times with different contexts.

`class Context(dict_=None)` The constructor of django.template.Context takes an optional argument — a dictionary mapping variable names to variable values.

`Template.render(context)` Call the Template object’s `render()` method with a Context to “fill” the template:

    >>> from django.template import Context, Template
    >>> template = Template("My name is {{ my_name }}.")

    >>> context = Context({"my_name": "Adrian"})
    >>> template.render(context)
    "My name is Adrian."

    >>> context = Context({"my_name": "Dolores"})
    >>> template.render(context)
    "My name is Dolores."




Unlike {{ MEDIA_URL }} ? Variables from settings.py aren't added automaticly to templates context.

Create a file called context_processors.py and write the following context processor:

from django.conf import settings

def cardspring(request):
    return { 'CARDSPRING_APP_ID': settings.CARDSPRING_APP_ID }

Then add your.location.context_processors.cardspring to TEMPLATE_CONTEXT_PROCESSORS in your Django settings file, where your.location is the location of your context_processors.py file.
