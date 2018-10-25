The DOM is a programming interface for HTML and XML documents is an essential part of making websites interactive.
It is an interface that allows a programming language to manipulate the content, structure, and style of a website.

In addition to parsing the style and structure of the HTML and CSS, the browser creates a representation of the document (the DOM).
The DOM represents the document as nodes and objects. That way, programming languages can connect to the page.
The DOM model represents a document with a logical tree. Each branch of the tree ends in a node,
and each node contains objects. DOM methods allow programmatic access to the tree;
with them you can change the document's structure, style or content.
Nodes can have event handlers attached to them. Once an event is triggered, the event handlers get executed.

To view exactly what the DOM is, in your web browser, right click on the current web page select Inspect. This will open up Developer Tools. The HTML code you see here is the DOM.

Each HTML element is considered a node in the DOM - an object that JavaScript can touch. These objects are arranged in a tree structure, with <html> being closer to the root, and each nested element being a branch further along the tree. JavaScript can add, remove, and change any of these elements.

If you right click on the site again and click View Page Source, you will see the raw HTML output of the website. It's easy at first to confuse the DOM with the HTML source, but they're different - the page source is exactly what is written in the HTML file. It is static and will not change, and will not be affected by JavaScript. The DOM is dynamic, and can change.

The outermost layer of the DOM, the layer that wraps the entire <html> node, is the document object. To begin manipulating the page with jQuery, we need to ensure the document is "ready" first, or JavaScript runs as page loaded.

Let's demonstrate how the DOM can be modified by client-side JavaScript. Type the following into the console:

    > document.body;

    <body>
      <h1>Document Object Model</h1>
    </body>

document is an object, body is a property of that object that we have accessed with dot notation.
In the console, we can change some of the live properties of the body object on this website. We'll edit the style attribute, changing the background color to fuchsia:

    > document.body.style.backgroundColor = 'fuchsia';

Switching to the Elements tab, or typing document.body into the console again, you will see that the DOM has changed:

    <body style="background-color: fuchsia;">
      <h1>Document Object Model</h1>
    </body>

Note: In order to change the background-color CSS property, we had to type backgroundColor in the JavaScript.
Any hyphenated CSS property will be written in camelCase in JavaScript.

However, right click on the page and select "View Page Source". You will notice that the source of the website does not contain the new style attribute we added via JavaScript. The source of a website will not change and will never be affected by client-side JavaScript.
If you refresh the page, the new code we added in the console will disappear.

Data Attributes
---------------

HTML5 is designed with extensibility in mind for data that should be associated with a particular element but need not have any defined meaning. data-* attributes allow us to store extra information on standard, semantic HTML elements

    <article
      id="electriccars"
      data-columns="3"
      data-index-number="12314"
      data-parent="cars">
    ...
    </article>

**Access in JavaScript**

To get a data attribute through the dataset object, get the property by the part of the attribute name after data- (note that dashes are converted to camelCase):

    var article = document.getElementById('electriccars');

    article.dataset.columns // "3"
    article.dataset.indexNumber // "12314"
    article.dataset.parent // "cars"

Two-way binding
-----------------
Means that:

When properties in the model get updated, so does the UI.

When UI elements get updated, the changes get propagated back to the model.

So any data-related changes affecting the model are immediately propagated to the matching view(s), and that any changes made in the view(s) (say, by the user) are immediately reflected in the underlying model. When app data changes, so does the UI, and conversely.

At its core, jQuery is used to connect with HTML elements in the browser via the DOM.
