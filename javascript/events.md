When a user clicks a button or presses a key, an event is fired. An event handler is a JavaScript function that runs when an event fires.
An event listener attaches a responsive interface to an element, which allows that particular element to wait and "listen" for the given event to fire.
There are three ways to assign events to elements:

**Inline Event Handler Attributes**

    <button onclick="changeText()">Click me</button>

it is more feasible to maintain JavaScript that is handled entirely through a separate script file than add handlers to every element.

**Event Handler Properties**

    <body>
        <button>Click me</button>
        <p>I will change.</p>
    </body>

    const changeText = () => {
        const p = document.querySelector('p');
        p.textContent = "I changed because of an event handler property.";
    }

    // Add event handler as a property of the button element
    const button = document.querySelector('button');
    button.onclick = changeText;

The event handler property is slightly more maintainable than the inline handler, but it still suffers from some of the same hurdles.

**Event Listeners**

Instead of assigning the event directly to a property on the element, we will use the addEventListener() method to listen for the event.

`addEventListener()` takes two mandatory parameters — the event it is to be listening for, and the listener callback function.

    const changeText = () => {
        const p = document.querySelector('p');

        p.textContent = "I changed because of an event listener.";
    }

    // Listen for click event
    const button = document.querySelector('button');
    button.addEventListener('click', changeText);

Often, anonymous functions will be used instead of a function reference on an event listener.

    button.addEventListener('click', () => {
        p.textContent = "Will I change?";
    });

AJAX
----
he jQuery `ajax()` method returns a Promise object. Using Promises with Ajax allows us to bind multiple callback functions to our request, write flexible code where our ajax handling logic is in a different place than our actual request, and wait for multiple requests to complete before starting an action.

Here is an example of separating the handling logic from the actual request:

    function getName(personid) {
       var dynamicData = {};
       dynamicData["id"] = personID;
       // Returns the jQuery ajax method
       return $.ajax({
           url: "getName.php",
           type: "get",
           data: dynamicData
       });
    }

    getName("2342342").done(function(data) {
        // Updates the UI based the ajax result
        $(".person-name").text(data.name);
    });

Since our function returns the jQuery `ajax()` method (which returns a Promise by default), we are able to call the `done()` method and pass a callback function (which will execute once the request has completed).

If we had wanted to wait for two separate ajax requests to our endpoint, we could have done something like this:

     function getName(personid) {
        var dynamicData = {};
        dynamicData["id"] = personID;
        // Returns the jQuery ajax method
        return $.ajax({
            url: "getName.php",
            type: "get",
            data: dynamicData
        });
    }

    var person1 = getName("2342342"),
        person2 = getName("3712968"),
        people = [person1, person2];

    $.when.apply(this, people).then(function() {
        // Both the ajax requests have completed
    });

We are using the JavaScript apply() method in the previous example to demonstrate how we can pass an array to the $.when method. If you do not want to use an array, then you can very easily pass each promise object (stored in a variable) as regular parameters.

IIFEs
-----

IIFEs are an ideal solution for locally scoping global variables/properties and protecting your JavaScript codebase from outside interference (e.g. third-party libraries). If you are writing jQuery code that will be run in many different environments (e.g. jQuery plugins), then it is important to use an IIFE to locally scope jQuery.
Here is how you would do it:

     // IIFE - Immediately Invoked Function Expression
    (function($, window, document) {
        // The $ is now locally scoped

      // The rest of your code goes here!

    }(window.jQuery, window, document));
    // The global jQuery object is passed as a parameter



