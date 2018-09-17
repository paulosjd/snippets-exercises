A runtime environment that allows developers to create all kinds of server-side tools and applications in JavaScript. The runtime is intended for use outside of a browser context (i.e. running directly on a computer or server OS). As such, the environment omits browser-specific JavaScript APIs and adds support for more traditional OS APIs including HTTP and file system libraries.

Benefits: performance, avoiding "context shift" between languages when you're writing both client-side and server-side code,

The node package manager (NPM) provides access to hundreds of thousands of reusable packages. You can use Node.js to create a simple web server using the Node HTTP package.

    // Load HTTP module
    var http = require("http");

    // Create HTTP server and listen on port 8000 for requests
    http.createServer(function(request, response) {

       // Set the response HTTP header with HTTP status and Content type
       response.writeHead(200, {'Content-Type': 'text/plain'});

       // Send the response body "Hello World"
       response.end('Hello World\n');
    }).listen(8000);

    // Print URL for accessing server
    console.log('Server running at http://127.0.0.1:8000/');

Save the file in the folder you created above. Go back to the terminal and type the following command and then navigate to "http://localhost:8000" in your web browser

    $ node "hello.js"

Other common web-development tasks are not directly supported by Node itself. If you want to add specific handling for different HTTP verbs (e.g. GET, POST, DELETE, etc.), separately handle requests at different URL paths ("routes"), serve static files, or use templates to dynamically create the response, then use a web framework:

**Express**

A framework which provides following mechanisms (similar to what e.g. Flask would provide):

Write handlers for requests with different HTTP verbs at different URL paths (routes).

Integrate with "view" rendering engines in order to generate responses by inserting data into templates.

Set common web application settings like the port to use for connecting, and the location of templates that are used for rendering the response.

Add additional request processing "middleware" at any point within the request handling pipeline.

While Express itself is fairly minimalist, developers have created compatible middleware packages to address almost any web development problem. There are libraries to work with cookies, sessions, user logins, URL parameters, POST data, security headers, and many more.

Opinionated frameworks are those with opinions about the "right way" to handle any particular task. They often support rapid development in a particular domain (solving problems of a particular type) because the right way to do anything is usually well-understood and well-documented. However they can be less flexible at solving problems outside their main domain.
Express is unopinionated, so has far fewer restrictions on the best way to glue components together to achieve a goal, or even what components should be used. They make it easier for developers to use the most suitable tools to complete a particular task, albeit at the cost that you need to find those components yourself.

    var express = require('express');
    var app = express();

    app.get('/', function(req, res) {
      res.send('Hello World!');
    });

    app.listen(3000, function() {
      console.log('Example app listening on port 3000!');
    });

If you have Node and Express already installed, run: `$ ./app.js`

The first two lines `require()` (import) the express module and create an Express application.

This object, which is traditionally named app, has methods for routing HTTP requests, configuring middleware, rendering HTML views, registering a template engine, and modifying application settings.

The middle part of the code shows a route definition. The `app.get()` method specifies a callback function that will be invoked whenever there is an HTTP GET request with a path ('/') relative to the site root. The callback function takes a request and a response object as arguments, and simply calls `send()` on the response to return the string "Hello World!"
The final block starts up the server on port '3000' and prints a log comment to the console.

**Importing and creating modules**

Express itself is a module, as are the middleware and database libraries that we use in our Express applications.

    // Message.js
    module.exports = 'Hello world';

    //or

    exports = 'Hello world';

    // Now, import this message module and use it as shown below.
    // app.js
    var msg = require('./Messages.js');

    console.log(msg);

To make objects available outside of a module you just need to expose them as additional properties on the exports object. For example, the `square.js` module below is a file that exports `area()` and `perimeter()` methods:

    exports.area = function(width) { return width * width; };
    exports.perimeter = function(width) { return 4 * width; };




