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
