Regex
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


