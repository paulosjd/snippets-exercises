Creating a Production Build
---------------------------
`npm run build` creates a `build` directory.
There are three files (called chunks) that are generated and placed in `build/static/js`:
- `main.[hash].chunk.js` is your applications code (`App.js` etc.)
- `1.[hash].chunk.js` is your *vendor* code (modules you've imported from within node_modules)
- `runtime~main.[hash].js` is a small chunk of webpack runtime logic used to load and run your app.

**Static File Caching**

A unique hash appended to the filename, and generated based on the contents of the file, allows you to use aggressive
caching techniques to avoid the browser re-downloading your assets if the file contents haven't changed.

It's best practice to specify a `Cache-Control` header for `index.html`, as well as the files within `build/static`.
This header allows you to control the length of time that the browser as well as CDNs will cache your static assets.
[Further reading](https://jakearchibald.com/2016/caching-best-practices/).
Using `Cache-Control: max-age=31536000` for your `build/static` assets, and `Cache-Control: no-cache` for everything
else is a safe and effective starting point.

Deployment
----------
After running `npm run build`, set up HTTP server so visitors are served `index.html`, and requests to
static paths like `/static/js/main.<hash>.js` are served with the contents of the `/static/js/main.<hash>.js`.

**Static server**

For environments using Node, the easiest way to handle this would be to install serve and let it handle the rest:
[docs](https://facebook.github.io/create-react-app/docs/deployment#static-server).

**Other Solutions**

You don’t necessarily need a static server in order to run a cra project in production. It works just
as fine integrated into an existing dynamic one, e.g. Node and Express:
[docs](https://facebook.github.io/create-react-app/docs/deployment#other-solutions).

**Configuring Client-Side Routing**

The server needs to be configured to respond to a request to `/todos/42` by serving `index.html`.
Otherwise the server looks for the file `build/todos/42` and does not find it.

**Building for Relative Paths**

By default, cra produces a build assuming your app is hosted at the server root.
To override this, specify the homepage in your package.json, for example:
`"homepage": "http://mywebsite.com/relativepath",`.
This will let cra correctly infer the root path to use in the generated HTML file.

Note: If you are using `react-router@^4`, you can root `<Link>`s using the `basename` prop on any `<Router>`.
More information [here](https://reacttraining.com/react-router/web/api/BrowserRouter/basename-string). E.g:

    <BrowserRouter basename="/calendar"/>
    <Link to="/today"/> // renders <a href="/calendar/today">
