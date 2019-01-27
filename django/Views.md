CBV's have several advantages when compared to FBV’s:
Organization of code related to specific HTTP methods (GET, POST, etc.) can be addressed by separate methods instead of conditional branching. 
Object oriented techniques such as mixins (multiple inheritance) can be used to factor code into reusable components. 

The first step to replace view functions with the new view classes:

    class MyClassBasedView(View):
        def get(self, request):
            # behave exactly like old style views
            # except this is called only on get request
            return http.HttpResponse("Get")

        def post(self, request):
            return http.HttpResponse("Post")

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

`class` django.views.generic.base.TemplateView

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
  
 **Generic display views**

`class` django.views.generic.DetailView

While this view is executing, self.object will contain the object that the view is operating upon, so by default it will be accessible in the template as e.g. {{ object.some_attribute }}.
This view inherits methods and attributes from views and mixins including TemplateResponseMixin, BaseDetailView, SingleObjectMixin.

    Method Flowchart:
        dispatch()
        http_method_not_allowed()
        get_template_names()
        get_slug_field()
        get_queryset()
        get_object()
        get_context_object_name()
        get_context_data()
        get()
        render_to_response()

`class` django.views.generic.ListView

While this view is executing, self.object_list will contain the list of objects that the view is operating upon.
Parents include TemplateResponseMixin, BaseListView, MultipleObjectMixin.

    Method Flowchart:
        dispatch()
        http_method_not_allowed()
        get_template_names()
        get_queryset()
        get_context_object_name()
        get_context_data()
        get()
        render_to_response()

In the simplest implementation, just use 'model = MyModel' which is really just shorthand for saying queryset = MyModel.objects.all().
However, by using queryset to define a filtered list of objects you can be more specific about the objects that will be visible in the view

    class BookList(ListView):
        queryset = Book.objects.order_by('-publication_date')
        context_object_name = 'book_list'

CRUD Views
----------
The most basic CreateView: At the most basic level, provide CreateView's ModelFormMixin with the model or custom ModelForm class as documented here.
Your CreateView class would look something like the following

    class AuthorCreateView(CreateView):
        form_class = AuthorForm
        template_name = 'author_new.html'
        success_url = 'success'

With those 3 core attributes set, call it in your URLs.

    ('^authors/create/$', Author.AuthorCreateView.as_view()),

Render the page and you'll see your ModelForm passed to the template as form, handling the form validation step (passing in request.POST / re-render if invalid), as well as calling form.save() and redirecting to the success_url.

**Generic editing views**

`class` django.views.generic.FormView

A view that displays a form. On error, displays the form with validation errors; on success, redirects to a new URL.
Parents include TemplateResponseMixin, BaseFormView, FormMixin.

https://ccbv.co.uk/projects/Django/1.4/django.views.generic.edit/FormView/

    def form_invalid(self, form):
        # re-render form, with form.errors?
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view. form_class
        is an attribute of the FormView
        """
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

**Start overriding the class methods**

    class ContactView(FormView):
    
        template_name = 'contact.html'
        form_class = ContactForm
        success_url = '/thanks/'
    
        def form_valid(self, form):
            # This method is called when valid form data has been POSTed and should return an HttpResponse.
            form.send_email()
            return super(ContactView, self).form_valid(form)

To customize behavior, start overriding the methods documented for the mixins.
Remember that you simply need to return an HttpResponse from one of these methods just like any regular view function.
Example overriding form_invalid documented in ModelFormMixin:

    class AuthorCreateView(CreateView):
        form_class = AuthorForm
        template_name = 'author_new.html'
        success_url = 'success'

    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

This per-method overriding starts becoming extremely useful as your forms grow more advanced and ultimately lets you build huge forms with a handful of lines of code, overriding only what is necessary.

Say you want to pass your form custom parameters such as the request object (very common if you need access to the user in the form): you merely need to override get_form_kwargs.

    class MyFormView(FormView):
        def get_form_kwargs(self):
            # pass "user" keyword argument with the current user to your form
            kwargs = super(MyFormView, self).get_form_kwargs()
            kwargs['user'] = self.request.user

**Models and request.user**

To track the user that created an object using a `CreateView`, you can use a custom `ModelForm` to do this. First, add the foreign key relation to the model:

    class Author(models.Model):
        name = models.CharField(max_length=200)
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        # ...

In the view, ensure that you don’t include created_by in the list of fields to edit, and override form_valid() to add the user:

    class AuthorCreate(CreateView):
        model = Author
        fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

Note that you’ll need to decorate this view using `login_required()`, or alternatively handle unauthorized users in the `form_valid()`.

**AJAX example**

A simple example showing how you might go about implementing a form that works for AJAX requests as well as ‘normal’ form POSTs:

    from django.http import JsonResponse
    from django.views.generic.edit import CreateView
    from myapp.models import Author

    class AjaxableResponseMixin:
        """
        Mixin to add AJAX support to a form.
        Must be used with an object-based FormView (e.g. CreateView)
        """
        def form_invalid(self, form):
            response = super().form_invalid(form)
            if self.request.is_ajax():
                return JsonResponse(form.errors, status=400)
            else:
                return response

        def form_valid(self, form):
            # We make sure to call the parent's form_valid() method because
            # it might do some processing (in the case of CreateView, it will
            # call form.save() for example).
            response = super().form_valid(form)
            if self.request.is_ajax():
                data = {
                    'pk': self.object.pk,
                }
                return JsonResponse(data)
            else:
                return response

    class AuthorCreate(AjaxableResponseMixin, CreateView):
        model = Author
        fields = ['name']

Misc
-----

**method_decorator**

`@method_decorator` from django.utils.decoratorst transforms a function decorator into a method decorator so that it can be used on an instance method. For example:

    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator

    class ProtectedView(TemplateView):
        template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

To decorate every instance of a class-based view, you need to decorate the class definition itself. To do this you apply the decorator to the `dispatch()` method of the class.

Or, you can decorate the class instead and pass the name of the method to be decorated as a kwarg. If you have a set of common decorators used in several places, you can define a list or tuple of decorators and use this instead of invoking `method_decorator()` multiple times.

**Overriding methods**

`get()` is a top-level method, and there's one for each HTTP verb - `post()`, `patch()`, etc. You would override it when you want to do something before a request is processed by the view, or after. With a form view is loaded for the first time, not when the form is submitted.

    class MyView(TemplateView):
        # ... other methods

    def get(self, *args, **kwargs):
        print('Processing GET request')
        resp = super().get(*args, **kwargs)
        print('Finished processing GET request')
        return resp

`get_queryset()`  is Used by ListViews - it determines the list of objects that you want to display. By default it will just give you all for the model you specify. By overriding this method you can extend or completely replace this logic.

    class FilteredAuthorView(ListView):
        template_name = 'authors.html'
        model = Author

    def get_queryset(self):
        # original qs
        qs = super().get_queryset()
        # filter by a variable captured from url, for example
        return qs.filter(name__startswith=self.kwargs.name)

`get_context_data()` This method is used to populate a dictionary to use as the template context. ListViews for example will populate the result from `get_queryset()` as author_list (object_list?) in the above example. You will probably be overriding this method most often to add extra content to display in your templates.

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data

    <h1>{{ page_title }}</h1>
    <ul>
    {% for author in author_list %}
        <li>{{ author.name }}</li>
    {% endfor %}
    </ul>

Admin actions - Bulk editing

**Pagination**

Django provides a few classes that help you manage paginated data – that is, data that’s split across several pages, with “Previous/Next” links.

The Paginator class has this constructor:

`class Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)`

object_list: A list, tuple, QuerySet, or other sliceable object with a `count()` or `__len__()` method. For consistent pagination, QuerySets should be ordered, e.g. with an `order_by()` clause or with a default ordering on the model.

    from django.core.paginator import Paginator
    paginator = Paginator(queryset, 20)

Here we are telling Django to paginate our QuerySet in pages of 20 each.

    # count the number of elements in the paginator
    >>> paginator.count
    104
    >>> paginator.num_pages
    6
    >>> paginator.page_range
    range(1, 7)
    # returns a Page instance
    >>> paginator.page(2)
    <Page 2 of 6>
    >>> page.has_other_pages()
    True

    class TopicListView(ListView):
        model = Topic
        paginate_by = 20

        def get_queryset(self):
            self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
            queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
            return queryset

HTML templates need editing accordingly.

