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

So to make objects available outside of a module you just need to expose them as additional properties on the exports object. For example, the `square.js` module below is a file that exports `area()` and `perimeter()` methods:

    exports.area = function(width) { return width * width; };
    exports.perimeter = function(width) { return 4 * width; };

We can import this module using `require()`, and then call the exported method(s) as shown:

    var square = require('./square'); // name of the file without the optional .js file extension
    console.log('The area of a square with a width of 4 is ' + square.area(4));

If you want to export a complete object in one assignment instead of building it one property at a time, assign it to module.exports:

    module.exports = {
      area: function(width) {
        return width * width;
      },

      perimeter: function(width) {
        return 4 * width;
      }
    };

**Using asynchronous APIs**

JavaScript code frequently uses asynchronous rather than synchronous APIs for operations that may take some time to complete. A synchronous API is one in which each operation must complete before the next operation can start.

Using non-blocking asynchronous APIs is even more important on Node than in the browser because Node is a single-threaded event-driven execution environment. "Single threaded" means that all requests to the server are run on the same thread (rather than being spawned off into separate processes). This model is extremely efficient in terms of speed and server resources, but it does mean that if any of your functions call synchronous methods that take a long time to complete, they will block not just the current request, but every other request being handled by your web application.

An asynchronous API is one in which the API will start an operation and immediately return (before the operation is complete). The code below will print out "Second, First" because even though `setTimeout()` method is called first, and returns immediately, the operation doesn't complete for several seconds.

    setTimeout(function() {
       console.log('First');
       }, 3000);
    console.log('Second');

There are a number of ways for an asynchronous API to notify your application that it has completed. The most common way is to register a callback function when you invoke the asynchronous API, that will be called back when the operation completes. This is the approach used above.

Tip: Using callbacks can be quite "messy" if you have a sequence of dependent asynchronous operations that must be performed in order because this results in multiple levels of nested callbacks. This problem is commonly known as "callback hell". This problem can be reduced by good coding practices, using a module like async, or even moving to ES6 features like Promises.

**Creating route handlers**

    app.get('/', function(req, res) {
      res.send('Hello World!');
    });

The callback function takes a request and a response object as arguments. In this case, the method simply calls send() on the response to return the string "Hello World!" There are a number of other response methods for ending the request/response cycle, for example, you could call `res.json()` to send a JSON response or `res.sendFile()` to send a file.

The Express application object also provides methods to define route handlers for all the other HTTP verbs

Often it is useful to group route handlers for a particular part of a site together and access them using a common route-prefix (e.g. a site with a Wiki might have all wiki-related routes in one file and have them accessed with a route prefix of /wiki/). In Express this is achieved by using the `express.Router` object. E.g. create our wiki route in a module named wiki.js, and then export the Router object, as shown below:

    // wiki.js - Wiki route module

    var express = require('express');
    var router = express.Router();

    // Home page route
    router.get('/', function(req, res) {
      res.send('Wiki home page');
    });

    // About page route
    router.get('/about', function(req, res) {
      res.send('About this wiki');
    });

    module.exports = router;

To use the router in our main app file we would then `require()` the route module (wiki.js), then call `use()` on the Express application to add the Router to the middleware handling path. The two routes will then be accessible from /wiki/ and /wiki/about/.

    var wiki = require('./wiki.js');
    // ...
    app.use('/wiki', wiki);

**Using middleware**

Whereas route functions end the HTTP request-response cycle by returning some response to the HTTP client, middleware functions typically perform some operation on the request or response and then call the next function in the "stack", which might be more middleware or a route handler. The order in which middleware is called is up to the app developer.

Note: The middleware can perform any operation, execute any code, make changes to the request and response object, and it can also end the request-response cycle. If it does not end the cycle then it must call `next()` to pass control to the next middleware function (or the request will be left hanging).

To install the morgan HTTP request logger middleware: `$ npm install morgan`.
You could then call `use()` on the Express application object to add the middleware to the stack:

    var express = require('express');
    var logger = require('morgan');
    var app = express();
    app.use(logger('dev'));
    ...

Middleware and routing functions are called in the order that they are declared.  The only difference between a middleware function and a route handler callback is that middleware functions have a third argument next, which  middleware functions are expected to call if they are not that which completes the request cycle.

**Serving static files**

You can use the `express.static` middleware to serve static files, including your images, CSS and JavaScrip:

    app.use('/media', express.static('public'));

Now, you can load the files that are in the public directory from the /media path prefix.

    http://localhost:3000/media/images/dog.jpg
    http://localhost:3000/media/video/cat.mp4
    http://localhost:3000/media/cry.mp3

**Handling errors**

Errors are handled by one or more special middleware functions that have four arguments, instead of the usual three: (err, req, res, next). For example:

    app.use(function(err, req, res, next) {
      console.error(err.stack);
      res.status(500).send('Something broke!');
    });

These can return any content required, but must be called after all other `app.use()` and routes calls so that they are the last middleware in the request handling process!

 If you pass an error to `next()` and you do not handle it in an error handler, it will be handled by the built-in error handler. Note that 404 is not treated as an error.

**Using databases**

There are many options, including PostgreSQL, MySQL, Redis, SQLite, MongoDB, etc.
First install the database driver using NPM, e.g.: `$ npm install mongodb`

Connect to the database, and then CRUD operations:

    //for mongodb version 3.0 and up
    let MongoClient = require('mongodb').MongoClient;
    MongoClient.connect('mongodb://localhost:27017/animals', function(err, client){
       if(err) throw err;

       let db = client.db('animals');
       db.collection('mammals').find().toArray(function(err, result){
         if(err) throw err;
         console.log(result);
         client.close();
       });
    });

Another popular approach is to access your database indirectly via an ORM. In this approach you define your data as "objects" or "models" and the ORM maps these through to the underlying database format. This approach allows you to think in terms of JS objects rather than database semantics, and that there is an obvious place to perform validation and checking of incoming data.

**Rendering Views**

In your application settings code you set the template engine to use and the location where Express should look for templates using the 'views' and 'view engines' settings:

    var express = require('express');
    var app = express();

    // Set directory to contain the templates ('views')
    app.set('views', path.join(__dirname, 'views'));

    // Set view engine to use, in this case 'some_template_engine_name'
    app.set('view engine', 'some_template_engine_name');

Assuming that you have template files named "index.<template_extension>" for 'title' and "message", you would call `Response.render()` in a route handler function to create and send the HTML response:

    app.get('/', function(req, res) {
      res.render('index', { title: 'About dogs', message: 'Dogs rock!' });
    });
