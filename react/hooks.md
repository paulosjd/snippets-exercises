

[React hooks](https://reactjs.org/docs/hooks-overview.html) are a way to access
the core features of React such as state without writing a class component.

`useState`
-----------
`useState` is a hook that allows you to have state variables in functional components.
It takes the initial value of the state variable as an argument. You can pass it directly,
or use a function to lazily initialize the variable:

    const Message= () => {
       const [message, setMessage]= useState( '' );
       const [listState, setList] = useState( [] );
       const [msg, setMsg] = useState( () => expensiveComputation() );
    }

Returns a stateful value, and a function to update it.

During the initial render, the returned state (state) is the same as the value passed
as the first argument.

The state-setting function is used to update the state. It accepts a new state value
and enqueues a re-render of the component.

Example of a handler function:

    const [count, setCounter] = useState(0);
    const [moreStuff, setMoreStuff] = useState(...);

    const setCount = () => {
        setCounter(count + 1);
        setMoreStuff(...);
    };

    <button onClick={setCount}>Click me</button>


Snippets
--------

Q: To slowly migrate to hooks, can I add hooks into classes? A:
Higher order components are how we have been doing this type of thing until hooks came along. You can write a simple high order component wrapper for your hook.

    function withMyHook(Component) {
      return function WrappedComponent(props) {
        const myHookValue = useMyHook();
        return <Component {...props} myHookValue={myHookValue} />;
      }
    }

While this isn't truly using a hook directly from a class component, this will at least allow you to use the logic of your hook from a class component, without refactoring.

    class MyDiv extends React.Component {
      render(){
        const myHookValue = this.props.myHookValue;
        return <div>{myHookValue}</div>;
      }
    }

    MyDiv = withMyHook(MyDiv);

***






Custom Hook Examples
--------------------

**`useKeyPress` from [usehooks.com](https://usehooks.com/)**

This hook makes it easy to detect when the user is pressing a specific key on their keyboard.

    function App() {

      const happyPress = useKeyPress('h');
      const sadPress = useKeyPress('s');
      const robotPress = useKeyPress('r');
      const foxPress = useKeyPress('f');

      return (
        <div>
          <div>h, s, r, f</div>
          <div>
            {happyPress && '😊'}
            {sadPress && '😢'}
            {robotPress && '🤖'}
            {foxPress && '🦊'}
          </div>
        </div>
      );
    }

    function useKeyPress(targetKey) {

      const [keyPressed, setKeyPressed] = useState(false);

      // If pressed key is our target key then set to true
      function downHandler({ key }) {
        if (key === targetKey) {
          setKeyPressed(true);
        }
      }

      // If released key is our target key then set to false
      const upHandler = ({ key }) => {
        if (key === targetKey) {
          setKeyPressed(false);
        }
      };

      // Add event listeners
      useEffect(() => {
        window.addEventListener('keydown', downHandler);
        window.addEventListener('keyup', upHandler);

        // Remove event listeners on cleanup
        return () => {
          window.removeEventListener('keydown', downHandler);
          window.removeEventListener('keyup', upHandler);
        };
      }, []); // Empty array ensures that effect is only run on mount and unmount

      return keyPressed;
    }
