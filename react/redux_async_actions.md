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

When the above 'ageUp' function runs after a button click, the action gets dispatched and then it gets caught by 'ageUp' function
which catches the action then after the timeout dispatches another action which then reaches the reducer.

Now we can import our `actionCreators` and use them in our `mapDispatchToProps` (the second argument passed to `connect`, and used for dispatching actions):

![](../images/thunk3.png)

Recap on middleware:

Asynchronous middleware like redux-thunk or redux-promise wraps the store's `dispatch()` method and allows you to
dispatch something other than actions, for example, functions or Promises. Any middleware you use can then intercept
anything you dispatch, and in turn, can pass actions to the next middleware in the chain. For example, a Promise
middleware can intercept Promises and dispatch a pair of begin/end actions asynchronously in response to each Promise.
When the last middleware in the chain dispatches an action, it has to be a plain object.

Redux Docs Async Actions
------------------------
When you call an asynchronous API, the moment you start the call, and the moment when you receive an answer (or a timeout),
each will usually require a change in the application state.
To do that, you need to dispatch normal actions that will be processed by reducers synchronously.

This would involve at least three different kinds of actions to inform the reducer that either:

- The request began. Reducers may handle this action by toggling an `isFetching` flag in the state so the UI knows to show a spinner.

- The request finished successfully. May be handled by reducers by merging the new data into the state they manage and resetting `isFetching`.
The UI would hide the spinner, and display the fetched data.

- That the request failed. This action may be handled by resetting `isFetching`. Additionally, some reducers may want to store the error message so the UI can display it.

You may use a dedicated status field in your actions:

    { type: 'FETCH_POSTS' }
    { type: 'FETCH_POSTS', status: 'error', error: 'Oops' }
    { type: 'FETCH_POSTS', status: 'success', response: { ... } }

Or you can define separate types for them:

    { type: 'FETCH_POSTS_REQUEST' }
    { type: 'FETCH_POSTS_FAILURE', error: 'Oops' }
    { type: 'FETCH_POSTS_SUCCESS', response: { ... } }

Before rushing into the implementation, it's important to consider the shape of the application's state. E.g. for a 'Reddit Headlines' app:

    { selectedSubreddit: 'frontend',
      postsBySubreddit: {
        frontend: {
          isFetching: true,
          didInvalidate: false,
          items: []
        },
        reactjs: {
          isFetching: false,
          didInvalidate: false,
          lastUpdated: 1439478405547,
          items: [
            {id: 42, title: 'Confusion about Flux and Relay'},
            {id: 500, ...

For every list of items, you'll want to store `isFetching` to show a spinner, `didInvalidate`
so you can later toggle it when the data is stale,
In a real app, you'll also want to store pagination state like `fetchedPageCount` and `nextPageUrl`.

**Handling Actions**

In `reducers.js` we write functions which manage part of the state. Below we extract `posts(state, action)` that manages
the state of a specific post list. This is just reducer composition! It is our choice how to split the reducer into
smaller reducers, and in this case, we're delegating updating items inside an object to a `posts` reducer.

Remember that reducers are just functions, so you can use functional composition and higher-order functions.
`combineReducers()`, as described in  [Splitting Reducers](https://redux.js.org/basics/reducers#splitting-reducers) in the docs.

![](../images/reducers.png)

n.b. instead of `Object.assign()`, could use nicer object spread syntax  e.g. `{ ...state, didInvalidate: true}`

**Async Action Creators**

By using Redux Thunk middleware, an action creator can return a function instead of an action object.
This way, the action creator becomes a thunk.

When an action creator returns a function, that function will get executed by the middleware.
This function doesn't need to be pure; it is thus allowed to have side effects, including executing asynchronous API calls.
The function can also dispatch synchronous actions. Define these special thunk action creators inside our `actions.js` file:

![](../images/thunk5.png)

[Link](https://redux.js.org/advanced/async-actions#actionsjs-with-fetch) to example of a more sophisticated async control flow:




