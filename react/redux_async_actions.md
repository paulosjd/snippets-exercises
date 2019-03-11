Async actions and `applyMiddleware`
-----------------------------------

An example of an async action would be a user clicking on some button to change something in his profile.
So this involves saving this to the server, and once this async action is done/save confirmed, the state should be updated.
n.b. in the case of an error state would be in accordance.

To add the middleware, we need to go to index.js where we create our store, import `applyMiddleware` from redux and pass it to `createStore`
Middleware e.g. redux-thunk, lets you capture some action and do something with it before dispatching to the store.

https://redux.js.org/advanced/async-actions

**redux-thunk**

A principle of Redux (listed in the introduction section of the docs) is that 'changes are made with pure functions'.

Three states in an *asynchronous* process (e.g. AJAX request):

    store.dispatch({ type: 'LOAD_START' })
    fetch('/data.json')
      .then(data =>
        store.dispatch({ type: 'LOAD_FINISH', data: data }))
      .catch(error =>
        store.dispatch({ type: 'LOAD_ERROR', error: error }))

Let's try putting this logic in the reducer. Let's add `fetch()` into it.

    function reducer (state, action) {
      if (action.type === 'LOAD_START') {
        fetch('/data.json').then(??).catch(??)
        return { ...state, loading: true }  } else { return state } }
    createStore(reducer)

It seems you can't `dispatch()` inside a reducer!

This is how Redux was designed. Reducers only define how to move from one state to another; it can't have side effects.

† The “vanilla” store implementation you get by calling `createStore` only supports plain object actions and
hands them immediately to the reducer.

However, if you wrap createStore with `applyMiddleware`, the middleware can interpret actions differently,
and provide support for dispatching async actions. Async actions are usually asynchronous primitives like Promises, Observables, or thunks.

Meet redux-thunk, a Middleware, or a plugin that extends `dispatch()` to do more things.

    import reducer from "./store/reducers/reducer";
    import { Provider } from "react-redux";
    import { createStore, applyMiddleware } from 'redux'
    import thunk from 'redux-thunk'

    store = createStore(reducer, applyMiddleware(thunk))

    ReactDOM.render(
      <Provider store={store}>
        <App />
      </Provider>,
      document.getElementById("root")
    );

redux-thunk allows you to dispatch functions that can in turn dispatch actions (commonly used to make API calls):

thunk - statement wrapped with a function, so later call the function to return that statement to be executed.
So instead of dispatching action an right there, wrap it with a function (a thunk), then we call that function
to return those actions.

Consider this minimal React-Redux `App.js`:

![](../images/thunk.png)

To use redux-thunk middleware, firstly write our actions in `actions.js` which which we will later use in `App.js`:

![](../images/thunk2.png)




