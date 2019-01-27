Objects are one of the 6 primary types in JS. Note that the simple primitives (`string`, `number`, `boolean`, `null`, and `undefined`) are not themselves an `object`.

`function` is a sub-type of object (technically, a "callable object"). Functions in JS are said to be "first class" in that they are basically just normal objects (with callable behavior semantics bolted on), and so they can be handled like any other plain object.

Arrays are also a form of objects, with extra behavior.

**Built-in Objects**

`String`, `Number`, `Boolean`, `Object`, `Function`, `Array`, `Date`, `RegExp`, `Error`

Their names seem to imply they are directly related to their simple primitives counter-parts, but in fact, their relationship is more complicated

These built-ins have the appearance of being actual types, even classes as in traditional OOP languages.

But these are actually just built-in functions, each of which can be used as a constructor (function call with the `new` operator, with the result being a newly constructed `object` of the sub-type in question. For instance:

    var strPrimitive = "I am a string";
    typeof strPrimitive;							// "string"
    strPrimitive instanceof String;					// false

    var strObject = new String( "I am a string" );
    typeof strObject; 								// "object"
    strObject instanceof String;					// true

    // inspect the object sub-type
    Object.prototype.toString.call( strObject );	// [object String]

The primitive value `"I am a string"` is not an `object`, it's a primitive literal and immutable value. To perform operations on it, such as checking its length, accessing its individual character contents, etc, a `String` object is required.

Luckily, the language automatically coerces a `"string"` primitive to a `String` object when necessary, which means you almost never need to explicitly create the Object form. It is strongly preferred to use the literal form for a value, rather than the constructed object form.

The same sort of coercion happens between the number literal primitive `42` and the `new Number(42)` object wrapper, when using methods like `42.359.toFixed(2)`. Likewise for `Boolean` objects from "boolean" primitives.

`null` and `undefined` have no object wrapper form, only their primitive values. By contrast, Date values can only be created with their constructed object form, as they have no literal form counter-part.

`Objects`, `Arrays`, `Functions`, and `RegExps` are all objects regardless of whether the literal or constructed form is used.

Contents
--------
the contents of an object consist of values (any type) stored at specifically named locations, which we call properties.

Note that while we say "contents" which implies that these values are actually stored inside the object, this can be misleading. What is stored in the container are these property names, which act as pointers/references to where the values are stored.

For access, The `.a` syntax is usually referred to as "property" access, whereas the `["a"]` syntax is usually referred to as "key" access.

In objects, property names are always strings. Any other value besides a string (primitive) will first be converted to a string. This includes numbers.

**Property vs. Method**

It's tempting to think of the function as belonging to the object, and in other languages, functions which belong to objects (aka, "classes") are referred to as "methods".
Technically, functions never "belong" to objects, so saying that a function that just happens to be accessed on an object reference is automatically a "method" seems a bit of a stretch of semantics.
The safest conclusion is probably that "function" and "method" are interchangeable in JS.

**Arrays**

Arrays are objects, so even though each index is a positive integer, you can also add properties onto the array:

    var myArray = [ "foo", 42, "bar" ];

    myArray.baz = "baz";

    myArray.length;	// 3

    myArray.baz;	// "baz"

Notice that adding named properties does not change the reported length of the array.

**Duplicating objects**

It would seem like there should just be a built-in `copy()` method, right? It turns out that it's not that clear-cut.

A shallow copy is fairly understandable and has far less issues, so ES6 has now defined `Object.assign(..)`.

    var myObject = {
        a: 2,
        b: anotherObject,	// reference, not a copy!
        c: anotherArray,	// another reference!
        d: anotherFunction
    };

    var newObj = Object.assign( {}, myObject );

    newObj.a;						// 2
    newObj.b === anotherObject;		// true
    newObj.c === anotherArray;		// true
    newObj.d === anotherFunction;	// true

Iteration
---------
**ES6 `for..of` loop syntax**

The `for..of` loop asks for an iterator object (from a default internal function known as `@@iterator`) of the thing to be iterated, and the loop then iterates over the successive return values from calling that iterator object's `next()` method, once for each loop iteration.
Regular objects do not have a built-in `@@iterator` but you can define one for them.





