CBV's have several advantages when compared to FBV’s:
Organization of code related to specific HTTP methods (GET, POST, etc.) can be addressed by separate methods instead of conditional branching. 
Object oriented techniques such as mixins (multiple inheritance) can be used to factor code into reusable components. 

**Base views**

Many of Django’s built-in class-based views inherit from other class-based views or various mixins. Because this inheritance chain is very important 

`class` django.views.generic.base.View

The master class-based base view. All other class-based views inherit from this base class.

    class MyView(View):
        def get(self, request, *args, **kwargs):
            return HttpResponse('Hello, World!')

`as_view`(**initkwargs)

A class method that returns a callable view which is able to take a request and return a response: 

	response = MyView.as_view()(request)

This method which returns a function (which the Django URL resolver expects) that can be called when a request arrives for a URL matching the associated pattern. This creates an instance of the class and calls its `dispatch()` method which looks at the request to determine whether it is a `GET`, `POST`, etc, and relays the request to a matching method if one is defined, or raises `HttpResponseNotAllowed` if not allowed.

The view returned view has view_class and view_initkwargs attributes.
When the view is called during the request/response cycle, the HttpRequest is assigned to the view’s request attribute. Then `dispatch()` is called:

    Method Flowchart:
        dispatch()
        http_method_not_allowed()
        options()

`dispatch(request, *args, **kwargs)`is
The view part of the view – the method that accepts a request argument plus arguments, and returns a HTTP response.
The default implementation will inspect the HTTP method and attempt to delegate to a method that matches the HTTP method; a GET will be delegated to `get()`, a POST to `post()`, and so on.

`http_method_not_allowed(request, *args, **kwargs)`is called instead if the view was called with a HTTP method it doesn’t support

`options(request, *args, **kwargs)` handles responding to requests for the OPTIONS HTTP verb and returns a response with the Allow header containing a list of the view’s allowed HTTP method names.

**TemplateView**

class django.views.generic.base.TemplateView

Renders a given template, with the context containing parameters captured in the URL.
Ancestors (MRO)

This view inherits methods and attributes from the following views:

    django.views.generic.base.TemplateResponseMixin 
    django.views.generic.base.ContextMixin 
    django.views.generic.base.View 
    
    class HomePageView(TemplateView):
        template_name = "home.html"
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['latest_articles'] = Article.objects.all()[:5]
            return context
        
Context: 
Populated (through ContextMixin) with the keyword arguments captured from the URL pattern that served the view.

Ancestors (MRO): This view inherits methods and attributes from the following view:
django.views.generic.base.View 

Note also that you can only inherit from one generic view - that is, only one parent class may inherit from View and the rest (if any) should be mixins. 