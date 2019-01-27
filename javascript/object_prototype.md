`[[Prototype]]` defines a "prototype chain" (somewhat similar to a nested scope chain) of objects to traverse for property resolution.

All normal objects have the built-in `Object.prototype` as the top of the prototype chain (like the global scope in scope look-up), where property resolution will stop if not found anywhere prior in the chain. This is why all objects can access `toString()`, `valueOf()`, etc.

While this resembles inheritance in OOP, the key distinction is that in JavaScript, no copies are made. Rather, objects end up linked to each other via an internal `[[Prototype]]` chain. So "delegation" is a more appropriate term than inheritance, because these relationships are not copies but delegation links.

**Prototypal Inheritance**

	function Foo(name) {
		this.name = name;
	}

	Foo.prototype.myName = function() {
		return this.name;
	};

	function Bar(name,label) {
		Foo.call( this, name );
		this.label = label;
	}

	// Object.setPrototypeOf( Bar.prototype, Foo.prototype );
	Bar.prototype = Object.create( Foo.prototype );

	Bar.prototype.myLabel = function() {
		return this.label;
	};

	var a = new Bar( "a", "obj a" );

	a.myName(); // "a"
	a.myLabel(); // "obj a"

**Inspecting "Class" Relationships**

Consider:

	function Foo() {
		// ...
	}

	Foo.prototype.blah = ...;

	var a = new Foo();

How do we then introspect `a` to find out its "ancestry"?:

	a instanceof Foo; // true

The question instanceof answers is: in the entire `[[Prototype]]` chain of `a`, does the object arbitrarily pointed to by `Foo.prototype` ever appear? The second, and much cleaner, approach to [[Prototype]] reflection is:

	Foo.prototype.isPrototypeOf( a ); // true

**`__proto__`**

	a.__proto__ === Foo.prototype; // true

The `.__proto__` property retrieves the internal `[[Prototype]]` of an object as a reference, allowing you to directly inspect (or even traverse: `.__proto__.__proto__...`) the chain.

Just as with `.constructor`, `.__proto__` doesn't actually exist on the object you're inspecting, it exists on the built-in `Object.prototype`, along with the other common utilities (`.toString()`, `.isPrototypeOf(..)`, etc).

	function Foo(name) { this.name = name; }
	var foo = new Foo('sam')
	h.prototype // undefined
	h.constructor //function Foo()
	h.constructor.prototype // Object { myName: myName(), … }
	h.__proto__ // Object { myName: myName(), … }

**`Object.create(..)`**

Creates a new object (`bar`) linked to the object we specified (`foo`), which gives us all the power (delegation) of the `[[Prototype]]` mechanism, but without any of the unnecessary complication of `new` functions acting as classes and constructor calls, confusing `.prototype` and `.constructor` references, or any of that extra stuff.

	var foo = {
		something: function() {
			console.log( "Tell me something good..." );
		}
	};

	var bar = Object.create( foo );

	bar.something(); ; // Tell me something good...

We don't *need* classes to create meaningful relationships between two objects. The only thing we should really care about is objects linked together for delegation, and `Object.create(..)` gives us that linkage without all the class cruft.

*n.b.* It may be tempting to think that these links between objects primarily provide a sort of fallback for "missing" properties or methods, however it's not very common or idiomatic in JS. For instance, call `bar.something()` and have that work even though there is no `something()` method on `myObject` introduces some "magic" into your API design that can be surprising for future developers who maintain your software.

You can however design your API with less "magic" to it, but still take advantage of the power of `[[Prototype]]` linkage:

	bar.doSomething = function() {
		this.something(); // internal delegation!
	};
	bar.doSomething(); ; // Tell me something good...

Ths makes our API design more explicit (less "magical"). Internally, our implementation follows the delegation design pattern, taking advantage of `[[Prototype]]` delegation to `foo.something()`.