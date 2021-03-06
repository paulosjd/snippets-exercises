﻿Regex
-----
    Metacharacters:  . ^ $ * + ? { } [ ] \ | ( )

Metacharacters are not active inside classes. For example, `[am$]` will match any of the characters 'a',  'm', or '$'.
You can match the characters not listed within the class by complementing the set. This is indicated by including a `'^'` as the first character of the class; e.g. `[^5]` will match any character except `'5'`.

Backslash remove special meaning, allow search of metacharacters in regex pattern, e.g. `\[` to search for square bracket.

    `\d` matches any digit, equiv. to [0-9]
    `\D` matches any non-digit, equiv. to [^0-9]
    `\s` and `\S` matches any whitespace character and matches non-whitespace
    `\w` matches any alphanumeric character; equiv to [a-zA-Z0-9_]
    `\W` matches any non-alphanumeric character; equiv to [^a-zA-Z0-9_]

    . matches anything except a newline
    | or operator. A|B will match any string that matches either A or B.

**Repetition**

`*` specifies that the previous character can be matched zero or more times, instead of exactly once. e.g. `ca*t` will match `ct` (0 a characters), `cat` (1 a), `caaat` (3 a characters). Repetitions such as `*` are greedy; - the matching engine will try to repeat it as many times as possible, if later portions do not match it will then back up and try again with few repetitions.

Consider the expression `a[bcd]*b` matching against the string `abcbd`. The engine matches [bcd]*, going as far as it can, which is to the end of the string.

Another repeating metacharacter is `+`, which matches one or more Whereas `*` matches zero or more times (so may not be present at all), `+` requires at least one occurrence.
The question mark character, `?`, matches either once or zero times; you can think of it as marking something as being optional.

The most complicated repeated qualifier is `{m,n}`, where `m` and `n` are decimal integers. This qualifier means there must be at least `m` repetitions, and at most `n`.

**Compiling Regular Expressions**

Regular expressions are compiled into pattern objects, allow e.g. searching for pattern matches or performing string substitutions.

    >>> p = re.compile('ab*', re.IGNORECASE)

    match()
    Determine if the RE matches at the beginning of the string.
    search()
    Scan through a string, looking for any location where this RE matches.
    findall(), finditer()
    Find all substrings where the RE matches, and returns them as a list or iterator.

**Module-Level Functions**

You don’t have to create a pattern object and call its methods; the re module also provides top-level functions called `match()`, `search()`, `findall()`, `sub()`, and so forth. These functions take the same arguments as the corresponding pattern method with the RE string added as the first argument, and still return either None or a match object instance.
Under the hood, these functions simply create a pattern object for you and call the appropriate method on it. There is little difference compared with
creating a pattern and calling it's methods, except for where access regex within a loop you may save number of function calls.

**Match objects**

    >>> p = re.compile('[a-z]+')
    >>> m = p.match('tempo')
    >>> m.group()
    'tempo'
    >>> m.start(), m.end()
    (0, 5)
    >>> m.span()
    (0, 5)

**Grouping**

`(` `)` have much the same meaning as they do in mathematical expressions; they group together the expressions contained inside them, and you can repeat the contents of a group with a repeating qualifier, such as `*`, `+`, `?`, or `{m,n}`.

    >>> p = re.compile('(a(b)c)d')
    >>> m = p.match('abcd')
    >>> m.groups()
    ('abc', 'b')
    >>> m.group()
    'abcd'
    >>> m.group(0)
    'abcd'
    >>> m.group(1)
    'abc'
    >>> m.group(2)
    'b'

**Lookahead Assertions**

`(?=...)` Positive lookahead assertion

`(?!...)` Positive lookahead assertion


Consider a simple pattern to match a filename and split it apart into a base name and an extension
The pattern to match this is quite simple: `.*[.].*$`

The `.` needs to be specially-treated as its a metacharacter. The trailing `$` is needed to ensure that all the rest of the string must be included in the extension. This regular expression matches foo.bar and autoexec.bat and sendmail.cf and printers.conf.

What if you want to match filenames where the extension is not bat? This is where a negative lookahead is used:

    .*[.](?!bat$).*$

The negative lookahead means: if the expression bat doesn’t match at this point, try the rest of the pattern; if bat$ does match, the whole pattern will fail. The trailing $ is required to ensure that something like sample.batch, where the extension only starts with bat, will be allowed.
The following pattern excludes filenames that end in either bat or exe:

    .*[.](?!bat$|exe$).*$

**Modifying Strings**

The `split()` method of a pattern splits a string apart wherever the RE matches occurs. There’s a module-level `re.split()` function, too.
Capturing groups can be used to determine the delimiter:

    >>> p2 = re.compile(r'(\W+)')
    >>> p2.split('This... is a test.')
    ['This', '... ', 'is', ' ', 'a', ' ', 'test', '.', '']

The `sub()` method of a pattern (and the module-level function) performs a similar task to `str.replace()`
For such operations, only use the re module where it is necessary.  Strings have several methods for performing operations with fixed strings and they’re usually much faster, because the implementation is a single small C loop that’s been optimized for the purpose, instead of the large, more generalized regular expression engine.

Dict constructor
---------------

    class dict(object)
     |  dict() -> new empty dictionary
     |  dict(mapping) -> new dictionary initialized from a mapping object's
     |      (key, value) pairs
     |  dict(iterable) -> new dictionary initialized as if via:
     |      d = {}
     |      for k, v in iterable:
     |          d[k] = v
     |  dict(**kwargs) -> new dictionary initialized with the name=value pairs
     |      in the keyword argument list.  For example:  dict(one=1, two=2)

    >>> dict([('a', 1)])
    {'a': 1}

    >>> dict([('a', 1)], b=2)
    {'a': 1, 'b': 2}

Example of dict constructor with both mapping and kwargs. This function
gives behavior like Enums, described in PEP 435:

    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        reverse = dict((value, key) for key, value in enums.iteritems())
        enums['reverse_mapping'] = reverse
        return type('Enum', (), enums)

    >>> numbers = enum('ZERO', 'ONE', 'TWO')
    >>> numbers.reverse_mapping
    {0: 'ZERO', 1: 'ONE', 2: 'TWO'}

    >>> numbers = enum('ZERO', 'ONE', foo='bar')
    >>> numbers.reverse_mapping
    {0: 'ZERO', 1: 'ONE', 'bar': 'foo'}

Local and Global Variables
--------------------------
Simply speaking a variable is an abstraction layer for the memory cells that contain the actual value.
Every module, class and function has its own namespace and variables are locally bound to that.

Generally, modifying global variables within functions is considered bad practice as it can lead to hard-to-detect side effects.

Descriptors
-----------
n.b. See 'Customizing Attribute Access' in python-data-model.ipynb for further reading.

Descriptors are a low-level mechanism that lets you hook into an object's attributes being accessed. Properties are a high-level application of this, and are preferable to writing descriptors if possible.

Therefore a descriptor is a way to customize what happens when you reference an attribute on a model.
E.g. you might need to validate the value that’s being assigned to a value.

Descriptors are implemented as classes and they are are assigned as attributes to other classes. The special methods `__get__`, `__set__`, `__delete__` are called automatically when the attribute is accessed.

    def expensive_func():
        return 'foo123'

    class CachedName(object):
        def __init__(self):
            self.name = 'instance_dict_key'

        def __get__(self, instance, owner):
            print(instance.__dict__)
            if self.name not in instance.__dict__:
                print('not in condition')
                instance.__dict__[self.name] = expensive_func()
                print(self.__dict__)
                print(instance.__dict__)
            return instance.__dict__[self.name]

        def __set__(self, instance, value):
            instance.__dict__[self.name] = ''.join([a for a in value if a.isalpha()])

    class MyClass:
        name = CachedName()

    m = MyClass()
    print('m.name is: {}'.format(m.name))
    m.name = 'foo1234'
    print('m.name is: {}'.format(m.name))

Given the following:

    class Foo(object):
        def __init__(self):
            self.x = 5

    f = Foo()

`f.x` would invoke `f.__getattribute__('x')`

The descriptor is slightly orthogonal; it is invoked by an attribute, rather than for an attribute.

Now, `f.x` would cause `type(f).__dict__['x'].__get__` to be called, and `f.x = 3` would call `type(f).__dict__['x'].__set__(3)`.
That is, `Foo.__getattr__` and `Foo.__getattribute__` would be used to find what f.x references; once you have that `__get__` and `__set__` are invoked if they are defined.

Put yet another way, if `MyDescriptor` did not define `__get__`, then `f.x` would simply return the instance of `MyDescriptor`

Context Managers
-----------------
See also [notes](https://github.com/paulosjd/snippets-exercises/blob/master/concepts_A-L.ipynb). "try..finally is good. with is better."
Also Yield in context managers in generators.md

A simple implementation of the `open()` context manager:

    class ManagedFile:
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            self.file = open(self.name, 'w')
            return self.file

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.file:
                self.file.close()

Our `ManagedFile` class follows the context manager protocol and now supports the `with` statement, just like `open()`:

    >>> with ManagedFile('hello.txt') as f:
    ...    f.write('hello, world!')

The `ManagedFile` context manager written using `contextlib.contextmanager` decorator:

    @contextmanager
    def managed_file(name):
        try:
            f = open(name, 'w')
            yield f
        finally:
            f.close()

    >>> with managed_file('hello.txt') as f:
    ...     f.write('hello, world!')
    ...     f.write('bye now')

*Side note on generators* The `yield` keyword turns a function into a generator.
When you call a generator function, instead of running the code immediately Python returns a
generator object, which is an iterator. An iterable object has a `__next__` method – allows
state to by maintained by processing one item at a time rather than just whole sequence from start to finish.

Above, `managed_file()` is a generator that first acquires the resource.
Then it temporarily suspends its own executing and yields the resource so it can be used by the
caller. When the caller leaves the with context, the generator continues to execute so that any
remaining clean up steps can happen

A context manager to change the current directory temporarily and then return to where you were:

    @contextmanager
    def working_directory(path):
        current_dir = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(current_dir)

    with working_directory("data/stuff"):
        # do something within data/stuff
    # here I am back again in the original working directory

Miscellaeneous Gotchas
----------------------

Immutable objects with same value always have the same hash in Python.

    some_dict = {}
    some_dict[5.5] = "Ruby"
    some_dict[5.0] = "JavaScript"
    some_dict[5] = "Python"

    >>> some_dict[5.5]
    "Ruby"
    >>> some_dict[5.0]
    "Python"
    >>> some_dict[5]
    "Python"

Python dictionaries check for equality and compare the hash value to determine if two keys are the same:

    >>> 5 == 5.0
    True
    >>> hash(5) == hash(5.0)
    True

The following behavior is due to CPython optimization (called string interning) that tries to use existing immutable objects in some cases rather than creating a new object every time.
After being interned, many variables may point to the same string object in memory (thereby saving memory).

    >>> a = "wtf"
    >>> b = "wtf"
    >>> a is b
    True

Strings that are not composed of ASCII letters, digits or underscores, are not interned.

    >>> a = "wtf!"
    >>> b = "wtf!"
    >>> a is b
    False

Bitwise operators
-----------------
The bitwise operators are similar to the logical operators, except that they work on binary representations of data. Bitwise operations are generally used in low level programming, e.g. such as networking, hardware register operations, data compression, and security/encryption operations. As such, they tend to be restricted to operating system and driver levels of code, embedded systems.
E.g. usually bitwise operations are faster than doing multiply/divide.

`and` tests whether both expressions are True in a boolean context while `&` will test if identity of both is `True`. Similar for `or` and `|`

    >>> a = True
    >>> b = True
    >>> a & b
    True
    >>> a = False
    >>> b = True
    >>> a & b
    False
    >>> a = 3
    >>> a | b
    3
    >>> b = 2
    >>> a & b
    2

The short-circuiting boolean operators (`and`, `or`) can't be overriden. & and | (and `not`, by the way) can be fully overriden, as they don't short circuit.

