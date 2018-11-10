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
The jQuery `ajax()` method returns a Promise object. Using Promises with Ajax allows us to bind multiple callback functions to our request, write flexible code where our ajax handling logic is in a different place than our actual request, and wait for multiple requests to complete before starting an action.

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

Hooks and callbacks
-------------------

A hook is essentially a place in code that allows you to tap in to a module to either provide different behavior or to react when something happens.
Tne good example of usage of hooks, coincidentally in web development, are WordPress' hooks. They are named appropriately in that they allow a way to 'hook into' certain points of the execution of a program.

So for example, the wp_head is an 'action' that is emitted when a WordPress theme is being rendered and it's at the part where it renders the part that's within the tags. Say that you want to write a plugin that requires an additional stylesheet, script, or something that would normally go within those tags. You can 'hook into' this action by defining a function to be called when this action is emitted. Something like:

    add_action('wp_head', 'your_function');

your_function() could be something as simple as:

    function your_function() {
        echo '<link rel="stylesheet" type="text/css" href="lol.css" />';
    }

Now, when WordPress emits this action by doing something like do_action('wp_head');, it will see that your_function() was 'hooked into' that action, so it will call that function (and pass it any arguments it may have).
Long story short: It allows you to add additional functionality at specific points of the execution of a program by 'hooking into' those points, in most cases by assigning a function callback.
In general, a callback is a function that you register with the API to be called at the appropriate time in the flow of processing.

A webhook is a general method for altering the behaviour of a web app with custom call. They are "user-defined HTTP callbacks", usually triggered by some event, such as pushing code to a repository or a comment being posted to a blog, and result in a HTTP POST payload being sent to the webhook's configured URL. Common uses are to trigger builds with continuous integration systems or to notify bug tracking systems.

**Callbacks in JavaScripts**

A callback function, also known as a higher-order function, is a function that is passed to another function as a parameter, and so the callback function is called (or executed) inside the other function.
Consider this common use of a callback function in jQuery:

    //The item in the click method's parameter is a function, not a variable.​
    //The item is a callback function
    $("#btn_1").click(function() {
    alert("Btn 1 Clicked");
    });

As you see in the preceding example, we pass a function as a parameter to the click method. And the click method will call (or execute) the callback function we passed to it. Note the way we pass an anonymous function (a function without a name) to the jQuery method as a parameter.

Callback Functions Are Closures - when we pass a callback function as an argument to another function, the callback is executed at some point inside the containing function’s body just as if the callback were defined in the containing function. This means the callback is a closure.

We can pass functions around like variables and return them in functions and use them in other functions. When we pass a callback function as an argument to another function, we are only passing the function definition. We are not executing the function in the parameter. In other words, we aren’t passing the function with the trailing pair of executing parenthesis () like we do when we are executing a function. And since the containing function has the callback function in its parameter as a function definition, it can execute the callback anytime.

`event.preventDefault()` vs. `return false`
-------------------------------------------
    $('a').click(function (e) {
        // custom handling here
        e.preventDefault();
    });

    $('a').click(function () {
    // custom handling here
    return false;
    });

`return false` from within a jQuery event handler is effectively the same as calling both `e.preventDefault` and `e.stopPropagation` on the passed `jQuery.Event` object. Note that for normal (non-jQuery) event handlers, `return false` does not stop the event from bubbling up.

The benefit to using `event.preventDefault()` is that you can add this as the first line in the handler, thereby guaranteeing that the anchor's default behavior will not fire, regardless if the last line of the function is not reached (eg. runtime error).



