https://facebook.github.io/react-native/docs/network.html

https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

How can I make an AJAX call in React?

You can use any AJAX library you like with React. Some popular ones are Axios, jQuery AJAX, and the browser built-in window.fetch.

window.fetch is a JS interface for accessing and manipulating requests and responses. It provides a global `fetch()` method that provides an easy, logical way to fetch resources asynchronously across the network.

    import React, { Component } from 'react';
    
    const API = 'https://hn.algolia.com/api/v1/search?query=';
    const DEFAULT_QUERY = 'redux';
    
    class App extends Component {
      constructor(props) {
        super(props);
    
        this.state = {
          hits: [],
        };
      }
    
      componentDidMount() {
        fetch(API + DEFAULT_QUERY)
          .then(response => response.json())
          .then(data => this.setState({ hits: data.hits }));
      }
    
      ...
    }
    
    export default App;

    function getMoviesFromApiAsync() {
       return fetch('https://facebook.github.io/react-native/movies.json')
       .then((response) => response.json())
       .then((responseJson) => {
         return responseJson.movies;
       })
       .catch((error) => {
         console.error(error);
       });
    }

    fetch('http://example.com/movies.json')
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        console.log(JSON.stringify(myJson));
      });

Above, `fetch()` returns a promise containing the response (a `Response` object).
   
To extract the JSON body content from the HTTP response, we use the `json()` method (defined on the Body mixin, which is implemented by both the `Request` and `Response` objects.)

![](../images/fetch.png)

**Example POST method implementation:**
    
    postData(`http://example.com/answer`, {answer: 42})
      .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
      .catch(error => console.error(error));
    
    function postData(url = ``, data = {}) {
      // Default options are marked with *
        return fetch(url, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, cors, *same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
                // "Content-Type": "application/x-www-form-urlencoded",
            },
            redirect: "follow", // manual, *follow, error
            referrer: "no-referrer", // no-referrer, *client
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json()); // parses response to JSON
    }

**Response Metadata**

    fetch('users.json').then(function(response) {
        console.log(response.headers.get('Content-Type'));
        console.log(response.status);
        console.log(response.type);
        console.log(response.url);
    });

`response.type` will be either of `"basic"`, `"cors"` or `"opaque"`.
You can define a mode for a fetch request such that only certain requests will resolve. The modes you can set include
`same-origin`, which only succeeds for requests for assets on the same origin, and
`cors` will allow requests for assets on the same-origin and other origins which return the appropriate CORs headers.

    fetch('http://some-site.com/cors-enabled/some.json', {mode: 'cors'})
      .then(function(response) {
        return response.text();
      })

**Chaining Promises**

If you are working with a JSON API, you'll need to check the status and parse the JSON for each response. You can simplify your code by defining the status and JSON parsing in separate functions which return promises, freeing you to only worry about handling the final data and the error case.

    function status(response) {
      if (response.status >= 200 && response.status < 300) {
        return Promise.resolve(response)
      } else {
        return Promise.reject(new Error(response.statusText))
      }
    }

    function json(response) {
      return response.json()
    }

    fetch('users.json')
      .then(status)
      .then(json)
      .then(function(data) {
        console.log('Request succeeded with JSON response', data);
      }).catch(function(error) {
        console.log('Request failed', error);
      });

The great thing with this is that you can share the logic across all of your fetch requests, making code easier to maintain, read and test.






