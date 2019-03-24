Classic example:

    def fib():
        a, b = 0, 1
        while True:
           yield b
           a, b = b, a+b

PEP255
-------

**Motivation**

When a producer function has a hard enough job that it requires maintaining state between values produced,
most programming languages offer no pleasant and efficient solution beyond adding a callback function to the
producer's argument list, to be called with each value produced.

**Specification: Yield**

The `yield` statement may only be used inside functions. A function that contains a `yield` statement is
a generator function. A generator function is an ordinary function object but are actually factory
functions that produce generator-iterators. In this respect they're radically different from
non-generator functions, acting more like a constructor than a function

When a generator function is called, the actual arguments are bound to function-local formal argument
names in the usual way, but no code in the body of the function is executed. Instead a generator-iterator
object is returned; this conforms to the iterator protocol, so in particular can be used in for-loops in a
natural way.

Note that the unqualified name "generator" may be used to refer either to a generator-function or a
generator-iterator. An iterator is an object with a `__next__` method.

Each time the `__next__` method of a generator-iterator is invoked, the code in the body of the
generator-function is executed until a yield or return statement is encountered, or until the end of the
body is reached.

If a yield statement is encountered, the state of the function is frozen, and the value of *expression_list*
is returned to `__next__`'s caller. By "frozen" we mean that all local state is retained: enough information
so that the next time `__next__` is invoked, the function can proceed exactly as if the yield statement
were just another external call.


21:00 if Beazley gen

1:01:00 yield from Beazley gen





