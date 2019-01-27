
Example of `request.path`

    {% block pagination %}
      {% if is_paginated %}
          <div class="pagination">
              <span class="page-links">
                  {% if page_obj.has_previous %}
                      <a href="{{ request.path }}?page={{ page_obj.previous_page_number }}">previous</a>
                  {% endif %}
                  <span class="page-current">
                      Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
                  </span>
                  {% if page_obj.has_next %}
                      <a href="{{ request.path }}?page={{ page_obj.next_page_number }}">next</a>
                  {% endif %}
              </span>
          </div>
      {% endif %}
    {% endblock %}

The `page_obj` is a `Paginator` object that will exist if pagination is being used on the current page. It allows you to get all the information about the current page, previous pages, how many pages there are, etc.

We use `{{ request.path }}` to get the current page URL for creating the pagination links. This is useful, because it is independent of the object that we're paginating.


`HttpRequest.is_ajax()`
-----------------------

Returns True if the request was made via an XMLHttpRequest, by checking the HTTP_X_REQUESTED_WITH header for the string 'XMLHttpRequest'. Most modern JavaScript libraries send this header.

Basic setup with ajax:

    urls.py

    url(r'^$', 'myapp.views.home', name='home'),
    url(r'^ajax_test/$', 'myapp.views.ajax_test', name='ajax_test'),

    views.py

    def home(request):
        return render_to_response('home.html', {},
                              context_instance=RequestContext(request))

    def ajax_test(request):
        if request.is_ajax():
            message = "This is ajax"
        else:
            message = "Not ajax"
        return HttpResponse(message)

    templates/home.html

    <!DOCTYPE html>
    <html>
    <head>
        <title></title>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    </head>
    <body>
    <script type="text/javascript">
        $(document).ready(function () {
            $.get("/ajax_test/", function (data) {
                alert(data);
            });
        });
    </script>
    </body>
    </html>

