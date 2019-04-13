**Connect: Dispatching Actions with `mapDispatchToProps`**

As the second argument passed in to `connect`, `mapDispatchToProps` is used for dispatching actions to the store.
With React Redux, your components never access the store directly - `connect` does it for you.
Often referred to as `mapDispatch` for short.

With it you gain the ability to pass down the action dispatching functions to child (likely unconnected)
components. This allows more components to dispatch actions, while keeping them "unaware" of Redux.

    const TodoList = ({ todos, toggleTodo }) => (
      <div>
        {todos.map(todo => (
          <Todo todo={todo} onClick={toggleTodo} />
        ))}
      </div>
    )

This is what React Redux’s connect does, it encapsulates the logic of talking to the Redux store and lets
you not worry about it.

The `mapDispatchToProps` parameter can be of two forms. While the function form allows flexibility in customizing
the functions your component receives, and how they dispatch actions, the object form is easier to use and is recommended if you can use it.

https://stackoverflow.com/questions/39419237/what-is-mapdispatchtoprops

What is mapDispatchToProps?

    const mapDispatchToProps = (dispatch) => {
      return {
        onTodoClick: (id) => {
          dispatch(toggleTodo(id))
        }
      }
    }

Understand in the context of the `container-component` pattern.
Your components are supposed to be concerned only with displaying stuff. The only place they are
supposed to get information from is their props. E.g.:

    class FancyAlerter extends Component {
        sendAlert = () => {
            this.props.sendTheAlert()
        }

        render() {
            <div>
              <h1>Today's Fancy Alert is {this.props.fancyInfo}</h1>
              <Button onClick={sendAlert}/>
            </div>
         }
    }

This component gets the info it displays from props (which came from the redux store via `mapStateToProps`)
and it also gets its action function from its props: `sendTheAlert()`.  It doesn't need to know about redux, store, dispatch, state etc.

That's where `mapDispatchToProps` comes in: in the corresponding `container`:

    // FancyButtonContainer.js

    function mapDispatchToProps(dispatch) {
        return({
            sendTheAlert: () => {dispatch(ALERT_ACTION)}
        })
    }

    function mapStateToProps(state} {
        return({fancyInfo: "Fancy this:" + state.currentFunnyString})
    }

    export const FancyButtonContainer = connect(
        mapStateToProps, mapDispatchToProps)(
        FancyAlerter
    )

`mapDispatchToProps` is the means that redux provides to let the container easily pass that function into the wrapped
component on its props. E.g. we are able to call `this.props.sendTheAlert` in the above component since it's defined
in the return value of `mapDispatchToProps`

`mapStateToProps`  doesn't have access to `dispatch`. So you couldn't use `mapStateToProps` to give the wrapped
component a method that uses `dispatch`. E.g. notice in the above component we access `this.props.fancyInfo`
that is defined in 'mapStateToProps'

**`mapStateToProps` example usage**

Import connect from react-redux and use it to connect the component with the state connect(mapStates,mapDispatch)(component)

    const MyComponent = (props) => {
        return (
          <div>
            <h1>{props.title}</h1>
          </div>
        );
      }
    }

Map the states to the props to access them with `this.props`

    const mapStateToProps = state => {
      return {
        title: state.title
      };
    };
    export default connect(mapStateToProps)(MyComponent);

Only the state that you map will be accessible via props.

**Context Usage**

In typical usage, your own components should never need to care about details of the store,
and won't ever reference it directly. React Redux handles these.

However, there may be certain use cases where you may need to customize how the store
and state are propagated to connected components, or access the store directly.
Internally, React Redux uses React's "context" feature to make the Redux store
accessible to deeply nested connected components.

React Redux's `<Provider>` component uses `<ReactReduxContext.Provider>` to put the
Redux store and the current store state into context, and `connect` uses `<ReactReduxContext.Consumer>`
to read those values and handle updates. Instead of using the default context instance
from React Redux, you may supply your own custom context
instance: [docs](https://react-redux.js.org/using-react-redux/accessing-store#providing-custom-context).


