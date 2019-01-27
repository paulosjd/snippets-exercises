
The first traditional phase of a standard language compiler is called lexing (aka, tokenizing), where tokens are assigned semantic meanings.
Lexical scope is based on where variables and blocks of scope are authored, by you, at write time.

![](../images/scope1.png)

Notice that these nested bubbles are strictly nested. In other words, no bubble for some function can simultaneously exist inside two other outer scope bubbles.

The structure and relative placement of these scope bubbles fully explains to the Engine all the places it needs to look to find an identifier.

In the above code snippet, the `Engine` executes the `console.log(..)` statement and goes looking for the three referenced variables `a`, `b`, and `c`. It first starts with the innermost scope bubble, the scope of the `bar(..)` function. It won't find `a` there, so it goes up one level, out to the next nearest scope bubble, the scope of `foo(..)`. It finds `a` there, and so it uses that `a`.

Scope look-up stops once it finds the first match. The same identifier name can be specified at multiple layers of nested scope, which is called "shadowing". Regardless, scope look-up always starts at the innermost scope being executed at the time, and works its way outward/upward until the first match, and stops.

Note: Global variables are also automatically properties of the global object (window in browsers, etc.), so it is possible to reference a global variable not directly by its lexical name, but instead indirectly as a property reference of the global object.

    window.a

This technique gives access to a global variable which would otherwise be inaccessible due to it being shadowed. However, non-global shadowed variables cannot be accessed.

The lexical scope look-up process only applies to first-class identifiers, such as the a, b, and c. If you had a reference to foo.bar.baz in a piece of code, the lexical scope look-up would apply to finding the foo identifier, but once it locates that variable, object property-access rules take over to resolve the bar and baz properties, respectively.

Functions As Scopes
--------------------

Wrapping a function declaration around some code will in effect hide it. This is useful in the design of software, such as the API for a module/object, so you only expose what is minimally necessary, and "hide" other variables or functions which may behave in unexpected ways.
Another benefit of "hiding" variables and functions inside a scope is to avoid unintended collision between two different identifiers with the same name, and  unexpected overwriting of values.

*Global "Namespaces"* - A particularly strong example of (likely) variable collision occurs in the global scope. Multiple libraries loaded into your program can quite easily collide with each other if they don't properly hide their internal/private functions and variables.
Such libraries typically will create a single variable declaration, often an object, with a sufficiently unique name, in the global scope. This object is then used as a "namespace" for that library, where all specific exposures of functionality are made as properties of that object (namespace)

As we have learnt, in the following `var a` within `foo()` will be hidden from the global scope:

    var a = 2;

    function foo() { // <-- insert this

        var a = 3;
        console.log( a ); // 3

    } // <-- and this
    foo(); // <-- and this

    console.log( a ); // 2

One issue with this however is that we have to declare a named-function `foo()`, which means that the identifier name `foo` itself "pollutes" the enclosing scope (global, in this case).

It would be more ideal if the function didn't need to "pollute" the global namespace and if the function could automatically be executed.
A solution is in function expressions:

    var a = 2;

    (function foo(){ // <-- insert this

        var a = 3;
        console.log( a ); // 3

    })(); // <-- and this

    console.log( a ); // 2

**Function declaration vs. function expression**

*Note*: The easiest way to distinguish declaration vs. expression is the position of the word "function" in the statement. If "function" is the very first thing in the statement, then it's a function declaration. Otherwise, it's a function expression.

The key difference we can observe here between a function declaration and a function expression relates to where its name is bound as an identifier.
Compare the previous two snippets. In the first snippet, the name `foo` is bound in the enclosing scope, and we call it directly with `foo()`. In the second snippet, the name `foo` is not bound in the enclosing scope, but instead is bound only inside of its own function.

**Anonymous function vs. named function**

Consider function expressions as callback parameters, e.g.:

    setTimeout( function(){
        console.log("I waited 1 second!");
    }, 1000 );

This is called an "anonymous function expression", because `function()`... has no name identifier on it. Function expressions can be anonymous, but function declarations cannot omit the name.

Anonymous function expressions are quick and easy to type, but draw-backs to consider are that they have no useful name to display in stack traces, which can make debugging more difficult. Also that a descriptive name helps self-document the code in question.

Inline function expressions are powerful and useful -- the question of anonymous vs. named doesn't detract from that. Providing a name for your function expression quite effectively addresses all these draw-backs, but has no tangible downsides. The best practice is to always name your function expressions:

    setTimeout( function timeoutHandler(){ // <-- Look, I have a name!
        console.log( "I waited 1 second!" );
    }, 1000 );

**IIFE's**

Now that we have a function as an expression by virtue of wrapping it in a `( )` pair, we can execute that function by adding another () on the end, like `(function foo(){ .. })()`. The first enclosing `( )` pair makes the function an expression, and the second `()` executes the function.

There's a slight variation on the traditional IIFE form: `(function(){ .. }())`. These two forms are identical in functionality.

Blocks As Scopes
----------------
While functions are the most common unit of scope, the usage of other scope units can lead to even better, cleaner to maintain code.

Consider the following:

    for (var i=0; i<2; i++) {
        console.log( i );
    };
    console.log( i ) // no ReferenceError

We declare the variable `i` directly inside the for-loop head, most likely because our intent is to use `i` only within the context of that for-loop. However we may not be aware that the variable actually scopes itself to the enclosing scope (function or global).

Block-scoping is all declaring variables as close as possible, as local as possible, to where they will be used.

On the surface, JS has no facility for block scope, until you dig a little further:

It's little known that JS in ES3 specified the variable declaration in the `catch` clause of a `try/catch` to be block-scoped to the `catch` block.

    try {
        undefined(); // illegal operation to force an exception!
    }
    catch (err) {
        console.log( err ); // works!
    }

    console.log( err ); // ReferenceError: `err` not found

**`let`**

The let keyword attaches the variable declaration to the scope of whatever block (commonly a `{ .. }` pair) it's contained in.
In addition, ES6 introduces `const`, which also creates a block-scoped variable, but whose value is fixed (constant).

Creating explicit blocks for block-scoping can address some of these concerns, making it more obvious where variables are attached and not. Usually, explicit code is preferable over implicit or subtle code.

    var foo = true;
    if (foo) {
        { // <-- explicit block
            let bar = foo * 2;
            console.log( bar );
        }
    }
    console.log( bar ); // ReferenceError

A particular case where let shines is in the for-loop case as we discussed previously.

    for (let i=0; i<10; i++) {
        console.log( i );
    }
    console.log( i ); // ReferenceError

Another reason block-scoping is useful relates to closures and garbage collection to reclaim memory.

Also, declarations made with `let` will not hoist to the entire scope of the block they appear in. Such declarations will not observably "exist" in the block until the declaration statement.

    {
       console.log( bar ); // ReferenceError!
       let bar = 2;
    }

-------------------------------------------------------------------------
**Hoisting**

There's a temptation to think that code in a JS program is interpreted line-by-line, top-down in order, as the program executes.

 Consider this code:

    a = 2;
    var a;
    console.log( a );

What do you expect to be printed in the `console.log(..)` statement?

To answer this question, recall that the `Engine` will compile code before it interprets it. Part of the compilation phase was to find and associate all declarations with their scopes. This is the heart of the lexical scope.

When you see: `var a = 2;`, JS actually thinks of it as two statements: `var a;` and `a = 2;`.

The first statement, the declaration, is processed during the compilation phase. The second statement, the assignment, is left in place for the execution phase.

Our first snippet then should be thought of as being handled like this:

    // compilation stage
    var a;

    // execution stage
    a = 2;
    console.log( a );  // 2

Consider another piece of code:

    console.log( a );
    var a = 2;

Handled like this:

    // compilation stage
    var a;

    // execution stage
    console.log( a );  // undefined
    a = 2;

Declarations themselves are hoisted, but assignments are not hoisted. Be careful about duplicate declarations,

Closures
--------
*Closure is when a function can remember and access its lexical scope even when it's invoked outside its lexical scope.*

    function foo() {
        var a = 2;

        function bar() {
            console.log( a );
        }

        return bar;
    }

    var baz = foo();

    baz(); // 2 -- Whoa, closure was just observed

Above, `bar()` is executed outside of its declared lexical scope.

By virtue of where it was declared, `bar()` has a lexical scope closure over that inner scope of `foo()`, which keeps that scope alive for `bar()` to reference at any later time.

`bar()` still has a reference to that scope, and that reference is called closure.

When the variable `baz` is invoked (invoking the inner function we initially labeled bar), it duly has access to author-time lexical scope, so it can access the variable `a` just as we'd expect.

The function is being invoked well outside of its author-time lexical scope. Closure lets the function continue to access the lexical scope it was defined in at author-time.

Closures enables patterns like *modules* in their various forms:

Modules
-------
Modules require two key characteristics: 1) an outer wrapping function being invoked, to create the enclosing scope 2) the return value of the wrapping function must include reference to at least one inner function that then has closure over the private inner scope of the wrapper.

Consider where we simply have some private data `something` and `another`, and a couple of inner functions `doSomething()` and `doAnother()`, which both have lexical scope and thus closure over the inner scope of `foo()`.

    function CoolModule() {
        var something = "cool";
        var another = [1, 2, 3];

        function doSomething() {
            console.log( something );
        }

        function doAnother() {
            console.log( another.join( " ! " ) );
        }

        return {
            doSomething: doSomething,
            doAnother: doAnother
        };
    }

    var foo = CoolModule();

    foo.doSomething(); // cool
    foo.doAnother(); // 1 ! 2 ! 3

The module instance is created when `CoolModule()` is invoked.
The object we return has references on it to our inner functions, but not to our inner data variables. We keep those hidden and private. It's appropriate to think of this object return value as essentially a public API for our module.

The `doSomething()` and `doAnother()` functions have closure over the inner scope of the module "instance".
When we transport those functions outside of the lexical scope, by way of property references on the object we return, we have now set up a condition by which closure can be observed and exercised.
