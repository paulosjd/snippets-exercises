Iterators
----------

The iterator protocol defines a standard way to produce a sequence of values.
An object is an iterator when it implements a `next()` method with the right semantics.
See also notes on [iterables and iterators](./js-objects).

Suppose `myFavouriteAuthors` is an object which contains another object `allAuthors`.
`allAuthors` contains three arrays with keys `crime`, `history`, and `travel`. How could
we iterate over the object to get all authors, other than writing a specific method for
this data structure?

Implementing the iteration protocol allows us to loop over our custom structure,
using syntax like `for (let author of myFavouriteAuthors) {...}`.

![](../images/iterator2.png)

Some statements and expressions expect iterables, e.g. `for-of` loops, spread syntax, `yield*`, and destructuring assignment
A `for-of` loop, for example, takes an *iterable* and creates
its *iterator* then keeps on calling the `next()` method until `done` is `true`.

Some built-in constructs, such as the spread syntax, use the same iteration protocol under the hood.

    [...'hi']  // [ "h", "i" ]

We can redefine the iteration behavior by supplying our own `@@iterator`:

    const someString = new String('hi');
    someString[Symbol.iterator] = () => {
      return {
        next: function() {  // ...
      }}
    }

**Iterable examples**

Built-in iterables

`String`, `Array`, `Map` and `Set` are all built-in iterables, because each of their prototype objects implements an `@@iterator` method.

User-defined iterables

    var myIterable = {};
    myIterable[Symbol.iterator] = function* () {
        yield 1;
        yield 2;
        yield 3;
    };
    [...myIterable]; // [1, 2, 3]

**Simple iterator examples**

An iterable's `@@iterator` method should return an iterator object

    const makeIterator = (array) => {
        var nextIndex = 0;
        return {
           next: () => {
               return nextIndex < array.length ?
                   {value: array[nextIndex++], done: false} :
                   {done: true};
           }
        };
    }

    const it = makeIterator(['hi', 'bye']);
    it.next().value // 'hi'
    it.next().value // 'bye'
    it.next().done  // true

The object created below satisfies both the iterator and iterable protocols:

    var myIterator = {
        next: () => { // ... },
        [Symbol.iterator]: () => { return this }
    };

This allows it to be consumed by syntaxes expecting iterables.

Generators
-----------
A generator is a function that can stop midway and then continue from where it stopped.
They are a special class of functions that simplify the task of writing iterators.
They produce a sequence of results instead of a single value.

    function* makeSimpleGenerator(array) {
        var nextIndex = 0;

        while (nextIndex < array.length) {
            yield array[nextIndex++];
        }
    }

    var gen = makeSimpleGenerator(['hi', 'bye']);

    gen.next().value // 'hi'
    gen.next().value // 'bye'
    gen.next().done  // true

For creating a generator function, we use `function*` syntax. Above where `makeSimpleGenerator` is invoked,
instead of returning any value, a generator function always returns a generator object.
The generator object is an iterator. So you can use it in `for-of` loops or constructs accepting an iterable.

When `yield`, execution of the function is paused and the value specified after it is returned/yielded.
Every function implicitly returns `undefined` if no `return` statement is provided.
Above, when `next()` is called and there are no more lines to execute,
the generator returns `{ value: undefined, done: true}`.
We’d now need to make new another generator object to reproduce this sequence of data.
We can also `return` from a generator. However, `return` sets the `done` property to `true` after
which the generator cannot generate any more values.

    function*  generatorFunc() {
      yield 'a';
      return 'b'; // Generator ends here.
      yield 'a'; // Will never be executed.
    }

**A generator object is both, iterator and iterable**

    var aGeneratorObject = function* () {
        yield 1;
        yield 2;
        yield 3;
    }();

It has a `next` method, so it's an iterator. Because it has an `@@iterator` method, it's also an iterable

    typeof aGeneratorObject.next  // "function"
    typeof aGeneratorObject[Symbol.iterator]  // "function"
    aGeneratorObject[Symbol.iterator]() === aGeneratorObject;
    // true, because its @@iterator method returns itself (an iterator), so it's an well-formed iterable
    [...aGeneratorObject];
    // [1, 2, 3]

Using the `function*` syntax makes it easy to implement iterables without having to write out `[Symbol.iterator]()` method which returns
an iterator object for which you need to `next()` method, like so

    const iterableObj = {
      [Symbol.iterator]() {
        let step = 0;
        return {
          next() {
            step++;
            if (step === 1) {
              return { value: 'This', done: false};
            } // ...
            return { value: '', done: true };
    }}}}

This is equivalent:

    function * iterableObj() {
      yield 'This';
      yield 'is';
      yield 'iterable.'
    }

**`yield*`**

The `yield*` expression is used to delegate to another iterable object:

    function* gen() {
          yield* [5, 10];
        }

    const iterator =  gen()
    iterator.next()  // { value: 5, done: false }
    iterator.next()  // { value: 10, done: false }
    iterator1.next()  // { value: undefined, done: true }

Or it can be used to delegate to another generator:

    function* func1() {
      yield 5;
      yield 10;
    }

    function* func2() {
      yield* func1();
    }

    const iterator = func2();
    iterator.next()  // { value: 5, done: false }
    iterator.next()  // { value: 10, done: false }
    iterator1.next()  // { value: undefined, done: true }

