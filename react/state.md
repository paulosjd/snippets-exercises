**Updating state with values that depend on the current state**

Pass a function instead of an object to `setState` to ensure the call always uses the most updated version of state

    incrementCount() {
      // Note: this will *not* work as intended.
      this.setState({count: this.state.count + 1});
    }

React doesn't update `this.state.count` until the component is re-rendered.
So above, `incrementCount()` ends up reading `this.state.count` as 0 every time.

Passing an update function allows you to access the current state value inside the updater. Since `setState` calls are batched, this lets you chain updates and ensure they build on top of each other instead of conflicting:

    incrementCount() {
      this.setState((state) => {
        // Important: read `state` instead of `this.state` when updating.
        return {count: state.count + 1}
      });
    }

*Currently*, `setState` is asynchronous inside event handlers. React “flushes” the state updates at the end of the browser event.




