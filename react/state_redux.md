
Redux
-----
[Cheatsheet](https://devhints.io/redux). 3 principles: A single source of truth. State is read-only. State is updated using pure functions


![](../images/redux.png)

![](../images/redux1a.jpg)

![](../images/redux2a.jpg)

![](../images/redux_disp_actions.png)

![](../images/redux3a.jpg)

So far we've learned about actions: things you `dispatch()` to a store to change its state.
Actions are dispatched whenever an event happens e.g., button clicked, page has finished loading, AJAX call has returned data.

    store.dispatch({ type: 'PUBLISH' })

Actions are objects and by convention always have a `type` key.

    const INITIAL_STATE = 0

    function increase() {
      return { type: 'INCREASE' }
    }

    function decrease() {
      return { type: 'DECREASE' }
    }

    function counterReducer(state = INITIAL_STATE, action = {}) {
      switch (action.type) {
        case INCREASE:
          return state + 1
        case DECREASE:
          return state - 1
        default:
          return state
      }
    }

    let { createStore, combineReducers } = Redux
    const rootReducer = combineReducers({ counter: counterReducer })
    const store = createStore(rootReducer)

    store.subscribe(() => {
      ReactDOM.render(
        <div>
          <pre>
            { JSON.stringify(store.getState(), null, 2) }
          </pre>
          <button
            onClick={ () => store.dispatch(increase()) }>
            Increase
          </button>
      </div>,
        document.getElementById('root')
      )
    })

**Actions and Reducers - Key Points**

Divide application into high-level stateful components and low-level stateless components.

Giving the Action a Name:

Define a constant to identify this action, can use a string initially, but use symbolic constants in namespaces eventually.

    // constants.js
    export const SET_SEARCH_TERM = "SET_SEARCH_TERM";

Create an Action Object:

Define a function to create an object representing an action. Put this in `actions.js` (in a small demo app):

    import CHANGE_SEARCHTERM from 'constants'

    export const setSearchTerm = (text) =>  { type: CHANGE_SEARCHTERM, payload: text }

Handle the Action:

Create the complement to our action generator in `reducers.js`. A constant defining the initial state…
that is the default value of reducer function’s state argument…and an action that tells the function how to update state:

    import { CHANGE_SEARCHTERM } from 'actions'

    const initialState = {
      searchTerm: ''
    }

    const robotsSearch = (state=initialState, action={}) => {
      switch (action.type) {
        case CHANGE_SEARCHTERM:
          return {...state, searchTerm: action.payload}
        default:
          return state
      }
    }

    export default robotsSearch;

If our reducer doesn’t recognize the action, it does nothing, which makes it safe for us to chain reducers together
Reducer functions always return a new state object. May recycle parts of the old state, but *never* mutate state in place

**redux-thunk**

Three states in an *asynchronous* process (e.g. AJAX request):

    store.dispatch({ type: 'LOAD_START' })
    fetch('/data.json')
      .then(data =>
        store.dispatch({ type: 'LOAD_FINISH', data: data }))
      .catch(error =>
        store.dispatch({ type: 'LOAD_ERROR', error: error }))

Let's try putting this logic in the reducer. Let's add `fetch() into it.

    function reducer (state, action) {
      if (action.type === 'LOAD_START') {
        fetch('/data.json').then(??).catch(??)
        return { ...state, loading: true }  } else {     return state   } }
    createStore(reducer)

It seems you can't `dispatch()` inside a reducer! This is how Redux was designed. Reducers only define how to move from one state to another; it can't have side effects.

Meet redux-thunk, a Middleware, or a plugin that extends `dispatch()` to do more things.

    import thunk from 'redux-thunk'
    import { createStore, applyMiddleware } from 'redux'

    store = createStore(reducer, {}, applyMiddleware(thunk))
    function load (dispatch, getState) {
      ...
    }
    store.dispatch(load)









You're talking about Redux and Redux-React (which provides the connect function, specifically for React components). Take a look at how Redux-React is implemented.

connect is just a React specific abstraction over subscribe.