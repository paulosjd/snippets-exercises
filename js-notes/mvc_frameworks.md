Where web applications are large scale and complex, JavaScript alone cannot be used to provide a stable foundation to write quality, maintainable code. As a result, new MVC frameworks have appeared that offer to provide structure and guidance when developing these applications.

MVC frameworks are libraries that can be included alongside JavaScript to provide a layer of abstraction on top of the core language. Their goal is to help structure the code-base and separate the concerns of an application into three parts:

    Model - Represents the data of the application. This matches up with the type of data a web application is dealing with, such as a user, video, picture or comment. Changes made to the model notify any subscribed parties within the application.
    View - The user interface of the application. Most frameworks treat views as a thin adapter that sits just on top of the DOM. The view observes a model and updates itself should it change in any way.
    Controller - Used to handle any form of input such as clicks or browser events. It’s the controller’s job to update the model when necessary (i.e. if a user changes their name).

Note that not all frameworks follow the MVC pattern. E.g. KnockoutJS uses the MVVM (Model - View - ViewModel) pattern.

Web applications are unlike a normal web page, they tend to feature more user interaction as well as needing to communicate with a backend server in real time. If you were to handle this behaviour without an MVC framework (i.e. just a DOM manipulation librarty like jQuery) you’d end up writing messy, unstructured, unmaintainable and untestable code.

If you are just building an application that still has a lot of the heavy lifting on the server-side (i.e. view generation) and there is little interaction on the client-side, you’ll find using an MVC framework is likely overkill.
Non-exhaustive checklist for where MVC framework may be necessary:

    Your application needs an asynchronous connection to the backend
    Your application has functionality that shouldn’t result in a full page reload (i.e. adding a comment to a post, infinite scrolling)
    Much of the viewing or manipulation of data will be within the browser rather than on the server
    The same data is being rendered in different ways on the page
    Your application has many trivial interactions that modify data (buttons, switches)

Some frameworks tend to be quite flexible in the way you can work with it, whereas others prefer you follow their predefined conventions. These differences can make a framework more suitable in certain scenarios than others.



KnockoutJS
----------
Example viewmodel:

    var myViewModel = {
        personName: 'Bob',
        personAge: 123
    };

You can then create a very simple view of this view model using a declarative binding. For example, the following markup displays the personName value:

The name is `<span data-bind="text: personName"></span>`

Computed Observables

Observables and dependency tracking is a core feature of KO. How can KO know when parts of your view model (dependencies) change? Answer: you need to declare your model properties as observables.

The `ko.computed()` takes a second parameter `this`. Without passing it in, it would not have been possible to refer to `this.day()`, `this.month()` or `this.year()`. In order to simplify things you can create a variable self, thus avoiding the addition of the second parameter. From now on we will use this approach in the code examples.

    function viewModel() {
      var self = this;
      self.day = ko.observable('24');
      self.month = ko.observable('02');
      self.year = ko.observable('2012');

      self.fullDate = ko.computed(function() {
       return self.day() + "/" + self.month() + "/" + self.year();
      });
    };

    ko.applyBindings(new viewModel());

**Knockout Overview**

Working with Knockout consists of several steps:

    Get data model. In most cases, data will be returned from the remote server in JSON format with AJAX call

    Create View. View is a HTML template with Knockout bindings, using “data-bind” attributes. It can contain divs, links, forms, buttons, images and other HTML elements for displaying and editing data.

    Create View Model. View model is a pure-code representation of the data operations on a UI. It can have usual properties and observable properties. An observable property means that when it’s changed in the view model, it will automatically be updated in the UI.

    Map data from data model to view model.

    Bind view model to the view. When view model is initialized, it can be bound to part of the HTML document, or the whole HTML document.

anonymous objects:

    var viewModel = {
           id = ko.observable(),
           title = ko.observable()
    }

Another way to create view models is to declare a function which can be reused:

    function ItemViewModel() {
         var self = this;
         self.id = ko.observable();
         self.title = ko.observable();
    }

    var viewModel = new ItemViewModel ();



