
**Why is binding necessary at all?**

These two code snippets are not equivalent:

    obj.method();

    var method = obj.method;
    method();

Above, `method` is a reference to the function which does not actually belong to `obj`. This is why you can borrow functions and call them from other objects. e.g.:

    class Obj{
        constructor(a){
            this.a = a
        }
        method(){
            return this.a + 1
        }
    }
    let obj = new Obj(2)
    let foo = {a: 3}
    let method2 = obj.method.bind(foo)
    alert(method2)  // 4

Binding methods helps ensure that the second snippet works the same way as the first one.
With React, typically you only need to bind the methods you pass to other components.

**Pass your components to to wrap them and give them the common functionality**

A runtime wrapper:

    const Wrapper = ({children}) => (
      <div>
        <div>header</div>
        <div>{children}</div>
        <div>footer</div>
      </div>
    );

    const App = () => <div>Hello</div>;

    const WrappedApp = () => (
      <Wrapper>
        <App/>
      </Wrapper>
    );

Initialization wrapper / HOC:

    // a function that takes a component and returns a new component
    const wrapHOC = (WrappedComponent) => (props) => (
      <div>
        <div>header</div>
        <div><WrappedComponent {...props}/></div>
        <div>footer</div>
      </div>
    )

    const App = () => <div>Hello</div>;

    const WrappedApp = wrapHOC(App);

**Rerender react component when prop changes**

    import equal from 'fast-deep-equal'  //  to compare the objects.

    constructor(){
      this.updateUser = this.updateUser.bind(this);
    }
    componentDidMount() {
      this.updateUser();
    }
    componentDidUpdate(prevProps) {
        // can also use some unique property,
        // e.g. (this.props.user.id !== prevProps.user.id)
        if(!equal(this.props.user, prevProps.user)) {
               this.updateUser();
        }
    }
    updateUser() {
      if (this.props.isManager) {
        this.props.dispatch(actions.fetchAllSites())
      } else {
        const currentUserId = this.props.user.get('id')
        this.props.dispatch(actions.fetchUsersSites(currentUserId))
      }
    }

**Transferring props**

It's a common pattern in React to wrap a component in an abstraction. You can use JSX spread attributes to merge the old props with additional values:

    <Component {...this.props} more="values" />

However, most of the time you should explicitly pass the properties down. This ensures that you only expose a subset of the inner API, one that you know will work.

    function FancyCheckbox(props) {
      var fancyClass = props.checked ? 'FancyChecked' : 'FancyUnchecked';
      return (
        <div className={fancyClass} onClick={props.onClick}>
          {props.children}
        </div>
      );
    }

**Curried function example**

    handleChange = field => e => {
        e.preventDefault()
        /// Do something here
    }

We'll start by representing it without using arrow functions …

    handleChange = function(field) {
      return function(e) {
        e.preventDefault()
        // Do something here
        // return ...
      };
    };

However, because arrow functions lexically bind this, it would actually look more like this …

    handleChange = function(field) {
      return function(e) {
        e.preventDefault()
        // Do something here
        // return ...
      }.bind(this)
    }.bind(this)

Maybe now we can see what this is doing more clearly. The `handleChange` function is creating a
function for a specified field. This is a handy React technique because you're required to setup
your own listeners on each input in order to update your applications state.
By using the `handleChange` function, we can eliminate all the duplicated code that would result
in setting up change listeners for each field.

Miscellaneous JSX notes
------------------------------------

**Props Default to “True”**

If you pass no value for a prop, it defaults to true. These two JSX expressions are equivalent:

    <MyTextBox autocomplete />

    <MyTextBox autocomplete={true} />

In general, we don’t recommend using this because it can be confused with the ES6 object shorthand `{foo}` which is short for `{foo: foo}` rather than `{foo: true}`. This behavior is just there so that it matches the behavior of HTML.

**Spread operator with props**

If you already have `props` as an object, and you want to pass it in JSX, you can use `...` as a “spread” operator to pass the whole props object. These two components are equivalent:

    function App1() {
      return <Greeting firstName="Ben" lastName="Hector" />;
    }

    function App2() {
      const props = {firstName: 'Ben', lastName: 'Hector'};
      return <Greeting {...props} />;
    }

**Children in JSX**

In JSX expressions that contain both an opening tag and a closing tag, the content between those tags is passed as a special prop: `props.children`. There are several different ways to pass children:

String literals (note that HTML is unescaped):

    <MyComponent>Hello world!</MyComponent>

    <div>This is valid HTML &amp; JSX at the same time.</div>

JSX Children (useful for displaying nested components):

    <MyContainer>
      <MyFirstComponent />
      <MySecondComponent />
    </MyContainer>

**JS expressions as children**

    function TodoList() {
      const todos = ['finish doc', 'submit pr', 'nag dan to review'];
      return (
        <ul>
          {todos.map((message) => <Item key={message} message={message} />)}
        </ul>
      );
    }

`export default`
----------------
![](../images/export.png)



