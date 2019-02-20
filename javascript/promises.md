**Introduction: callbacks**

![](../images/jscb2.png)

To handle errors:

    function loadScript(src, callback) {
      let script = document.createElement('script');
      script.src = src;

      script.onload = () => callback(null, script);
      script.onerror = () => callback(new Error(`Script load error for ${src}`));

      document.head.append(script);
    }

Here, So the single callback function is used both for reporting errors and passing back results.

**Callback hell**

The above style is fine for one or maybe two nested calls.
But for multiple asynchronous actions that follow one after another we’ll have code like this:

    loadScript('1.js', function(error, script) {
      if (error) {
        handleError(error);
      } else {
        // ...
        loadScript('2.js', function(error, script) {
          if (error) {
            handleError(error);
          } else {
            // ...
            loadScript('3.js', function(error, script) {
              if (error) {
                handleError(error);
              } else {
                // ...continue after all scripts are loaded (*)
              } ...

As calls become more nested, the code becomes deeper and increasingly more difficult to manage, especially if we have a real code instead of '...', that may include more loops, conditional statements etc.

We can try to alleviate the problem by making every action a standalone function, like this:

![](../images/jscb3.png)

**Promise basics**

    let promise = new Promise(function(resolve, reject) {
      // executor (the producing code)
    });

The function passed to `new Promise` is called the *executor*. When the promise is created, this executor function runs automatically. It contains the producing code, that should eventually produce a result.

The resulting promise object has internal properties: state and result.
When the executor finishes the job, it should call one of the functions that it gets as arguments

![](../images/promise.png)

![](../images/promise3.png)

The executor should call only one resolve or reject. The promise’s state change is final.
All further calls of resolve and reject are ignored. The idea is that a job done by the executor may have only one result or an error.
Further, resolve/reject expect only one argument and will ignore additional arguments.

Consumers: “then” and “catch”
---------------------------
A `Promise` object serves as a link between the executor (the “producing code”) and the consuming functions, which will receive the result or error. Consuming functions can be registered (subscribed) using the methods `.then` and `.catch`.

![](../images/promise6.png)

If we’re interested only in successful completions, then we can provide only one function argument to `.then`

If we’re interested only in errors, then we can use `null` as the first argument: `.then(null, errorHandlingFunction)`. Or we can use `.catch(errorHandlingFunction)`, which is exactly the same.

The call `.catch(f)` is a complete analog of `.then(null, f)`, it’s just a shorthand.

**On settled promises then runs immediately**

If a promise is pending, .then/catch handlers wait for the result. Otherwise, if a promise has already settled, they execute immediately:

    // an immediately resolved promise
    let promise = new Promise(resolve => resolve("done!"));
    promise.then(alert); // done! (shows up right now)

Some tasks may sometimes require time and sometimes finish immediately. The good thing is: the .then handler is guaranteed to run in both cases.

**Handlers of .then/.catch are always asynchronous**

Even when the Promise is immediately resolved, code which occurs on lines below your `.then/.catch` may still execute first.

![](../images/promise4.png)

The following example is the above callback example re-written:

![](../images/promise5.png)


