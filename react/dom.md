The virtual DOM
---------------
Aprogramming concept where an ideal, or “virtual”, representation of a UI is kept in memory and synced with the “real” DOM by
a library such as ReactDOM. This process is called reconciliation.

This approach enables the declarative API of React: You tell React what state you want the UI to be in, and it makes sure the
DOM matches that state. This abstracts out the attribute manipulation, event handling, and manual DOM updating that you would
otherwise have to use to build your app.

**Cost of calling `render()`**

There are two steps of what we may call "render":

- Virtual DOM render: when render method is called it returns a new virtual dom structure of the component.
- Native DOM render: React changes real DOM nodes in your browser only if they were changed in the Virtual DOM and as little as needed - this is that great React's feature which optimizes real DOM mutation and makes React fast.

Calling `render()` doesn't mean that DOM Nodes are being manipulated in any way. The render method just
serves the diff algorithm to decide which DOM Nodes need to really be attached / detached. Note that
`render()` is not expensive, it's the DOM manipulations that are expensive. They are executed only if
`render()` returns different virtual trees.

In the following example, the output depends on `props.imageUrl` and `props.username`. If in a parent
component you render `<UserAvatar username="fabio" imageUrl="http://foo.com/fabio.jpg" />`, so
always the same props, React would call `render` every time, even if the output would be exactly the same.

    class UserAvatar extends Component {
        render() {
           return <div><img src={this.props.imageUrl} /> {{ this.props.username }} </div>
        }
    }

React implements dom diffing, so the DOM would not be actually updated. Still, performing the dom diffing
in this scenario would be expensive and a waste. If the `UserAvatar` component extends `PureComponent` instead, a shallow compare is performed. And because
`props` and `nextProps` are the same, `render` will not be called at all.

Components, Elements, and Instances
-----------------------------------
**Managing the Instances**

Say if you declare a `Button` *component* by creating a class. When the app is running, you may have several *instances* of
this component on screen, each with its own properties and local state.

This is the traditional object-oriented UI programming. It is up to you to take care of creating and destroying child
component instances (e.g. button once form is submitted).
Each component instance has to keep references to its DOM node and to the instances of the children components, and many
lines of code needed grows with the number of possible states of the component
So how is React different?

**Elements Describe the Tree**

An element is a plain object describing a component instance or DOM node and its desired properties.
It contains only information about the component type (e.g. a Button), its properties, and any child elements inside it.

Elements are created using `React.createElement()`, or JSX more typicall. They are not actual instances. Rather, they tell
React what you want to see on the screen.

Elements can be either DOM Elements (when an element’s type is a string), or Component Elements (when the type is a
function or a class corresponding to a React component):

    {
      type: 'button',
      props: {
        className: 'button button-blue',
        children: {
          type: 'b',
          props: {
            children: 'OK!'
          }
        }
      }
    }

This element is just a way to represent the following HTML as a plain object:

    <button class='button button-blue'>
      <b>
        OK!
      </b>
    </button>

A component Element:

    {
      type: Button,
      props: {
        color: 'blue',
        children: 'OK!'
      }
    }

**Components Encapsulate Element Trees**

When React sees an element with a function or class `type`, it knows to ask that component what element it renders to,
given the corresponding `props`. When it sees this element:

    {
      type: Button,
      props: {
        color: 'blue',
        children: 'OK!'
      }
    }

React will ask `Button` what it renders to. The `Button` will return this element:

    {
      type: 'button',
      props: {
        className: 'button button-blue',
        children: {
          type: 'b',
          props: {
            children: 'OK!'
          }
        }
      }
    }

React will repeat this process until it knows the underlying DOM tag elements for every component on the page.
This is a part of the process that React calls reconciliation which starts when you call `ReactDOM.render()` or `setState()`.
By the end, React knows the result DOM tree, and a renderer like `react-dom` or `react-native` applies the minimal set of
changes necessary to update the DOM nodes.

Having mostly discussed elements and components, instances have much less importance in React than in most object-oriented
UI frameworks. Only components declared as classes have instances, and you never create them directly: React does that for you.

Refs
----
Refs provide a way to access DOM nodes or React elements created in the render method.

While there are a few good use cases for refs, e.g. managing focus and text selection, they should not be overused.
E.g. think more critically about where state should be owned in the component hierarchy. Often, it becomes clear that the
proper place to “own” that state is at a higher level in the hierarchy.

    class MyComponent extends Component {
      render () {
        return <div>
          <input ref={el => this.input = el} />
        </div>
      }

      componentDidMount () {
        this.input.focus()
      }
    }

When a ref is passed to an element in `render`, a reference to the node becomes accessible at the `current` attribute of
the ref. The value of the ref differs depending on the type of the node:

When the `ref` attribute is used on an HTML element, the `ref` created in the constructor with `React.createRef()`
receives the underlying DOM element as its `current` property.

When the `ref` attribute is used on a custom class component, the ref object receives the mounted instance of the
component as its `current`.

    class CustomTextInput extends React.Component {
        constructor(props) {
            super(props);
            // create a ref to store the textInput DOM element
            this.textInput = React.createRef();
            this.focusTextInput = this.focusTextInput.bind(this);
        }

        focusTextInput() {
            this.textInput.current.focus();
        }

        render() {
            return (
                <div>
                    <input
                        type="text"
                        ref={this.textInput} />
                    <input
                        type="button"
                        value="Focus the text input"
                        onClick={this.focusTextInput}
                    />
                </div>
            );
        }
    }

Fragments
---------
Used to return multiple children without adding extra wrapping nodes to the DOM. Example using the shorter syntax:

    class Columns extends React.Component {
      render() {
        return (
          <>
            <td>Hello</td>
            <td>World</td>
          </>
        );
      }
    }

Inline styles
-------------
    const style = { height: 10 }
    return <div style={style}></div>

    return <div style={{ margin: 0, padding: 0 }}></div>

**CSS `display:none` with a conditional**

    style={{display: this.state.showStore ? 'block' : 'none' }}

