
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