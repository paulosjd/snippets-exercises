**Spread/Rest**

When `...` is used in front of an array (actually, any iterable, which we cover in Chapter 3), it acts to "spread" it out into its individual values.

	function foo(x,y,z) {
		console.log( x, y, z );
	}

	foo.apply( null, [1,2,3] );		// 1 2 3

In the following usage, `...` acts to give us a simpler syntactic replacement for the `apply(..)` method:

	foo( ...[1,2,3] );				// 1 2 3

But `...` can be used to spread out/expand a value in other contexts as well, such as inside another array declaration:

	var a = [2,3,4];
	var b = [ 1, ...a, 5 ];
	console.log( b );		// [1,2,3,4,5]

In this usage, ... is basically replacing concat(..), as it behaves like [1].concat( a, [5] ) here.

The other common usage of ... can be seen as essentially the opposite; instead of spreading a value out, the ... gathers a set of values together into an array. Consider:

	function foo(x, y, ...z) {
		console.log( x, y, z );
	}

	foo( 1, 2, 3, 4, 5 );			// 1 2 [3,4,5]

	function foo(...args) {
		console.log( args );
	}

	foo( 1, 2, 3, 4, 5);			// [1,2,3,4,5]


**Default Parameters**

The boolean operators in JavaScript can be used where you need to get the first truthy or falsy value among a set of values, making it it easier to assign a default value. For default parameters

	function foo(x = 11, y = 31) {
		console.log( x + y );
	}

	foo();					// 42
	foo( 5, 6 );			// 11
	foo( 0, 42 );			// 42

	foo( 5 );				// 36
	foo( 5, undefined );	// 36 <-- `undefined` is missing
	foo( 5, null );			// 5  <-- null coerces to `0`

	foo( undefined, 6 );	// 17 <-- `undefined` is missing
	foo( null, 6 );			// 6  <-- null coerces to `0`

**What is a Function Declaration?**

A Function Declaration defines a named function variable without requiring variable assignment. Function Declarations occur as standalone constructs and cannot be nested within non-function blocks. It’s helpful to think of them as siblings of Variable Declarations. Just as Variable Declarations must start with “var”, Function Declarations must begin with “function”.

    function bar() {
        return 3;
    }

**What is a Function Expression?**

A Function Expression defines a function as a part of a larger expression syntax (typically a variable assignment ). Functions defined via Functions Expressions can be named or anonymous

    //anonymous function expression
    var a = function() {
        return 3;
    }

    //named function expression
    var a = function bar() {
        return 3;
    }

    //self invoking function expression
    (function sayHello() {
        alert("hello!");
    })();

Typically functions created by Function Expressions are unnamed. However, debugging with anonymous functions can be frustrating.