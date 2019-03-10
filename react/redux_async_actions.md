Async actions and `applyMiddleware`
------------------------------------
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

It seems you can't `dispatch()` inside a reducer! This is how Redux was designed. Reducers
only define how to move from one state to another; it can't have side effects.

† The “vanilla” store implementation you get by calling createStore only supports plain object actions and hands them immediately to the reducer.

However, if you wrap createStore with applyMiddleware, the middleware can interpret actions differently, and provide support for dispatching async actions. Async actions are usually asynchronous primitives like Promises, Observables, or thunks.

Meet redux-thunk, a Middleware, or a plugin that extends `dispatch()` to do more things.
redux-thunk allows you to dispatch functions that can in turn dispatch actions (commonly used to make API calls):

    import thunk from 'redux-thunk'
    import { createStore, applyMiddleware } from 'redux'

    store = createStore(reducer, {}, applyMiddleware(thunk))
    function load (dispatch, getState) {
      ...
    }
    store.dispatch(load)

