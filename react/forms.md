Because form elements naturally keep some internal state, HTML form elements work a little bit differently from other DOM elements in React.
To handle form submission with JS, the standard way is using “controlled components”

**Controlled Components**

In HTML, form and control elements such as `<input>`, `<textarea>`, and `<select>` typically maintain their own state and update it based on user input.
We can combine it with the React state which can be the “single source of truth”.

![](../images/react-form.png)

We use callback functions to handle form events and then use the container’s state to store the form data.
Since the `value` attribute is set on our form element, the displayed value will always be `this.state.value`, making the React state the source of truth. Since `handleChange` runs on every keystroke to update the React state, the displayed value will update as the user types.
An input form element whose value is controlled by React in this way is called a “controlled component”.

A recommended architecture is to give each form element a component of its own, which can be
reused in container components which house business logic, taking care of updating the state of the form, handling form submission, and making API calls/dispatching Redux actions.
The so-called regular, or dumb, components receive data from their parent (container) component. Dumb components are concerned with presentation and contain the actual DOM markup. They may trigger logic, like updating state, but only by means of functions passed down to them.

![](../images/formjs2.png)




![](../images/react-form3.png)



PropTypes
---------


