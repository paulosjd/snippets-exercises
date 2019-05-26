

String encoding
---------------

Character encoding is about translating characters into a unique sequence of bits.
A bit, the most fundamental piece of computer information,
is a signal that has only two possible states (2^1). 8 bits (a byte) lets
you express (2^8) 256 possible values, and so on.
You can express the numbers 0 and 1 with just 1 bit,
or you can use 8 bits to express them as 00000000 and 00000001.

You can express the numbers 0 to 3 with 2 bits, using 00 to 11, or as 8 bits
using leading zeroes. The highest ASCII code point, 127, requires only 7 significant bits.
Various informal and conflicting encodings arose with ASCII due to differences in
additional characters used with the 128 remaining code points.

**Integer literals** are used to express that an integer is typed in a base other than 10.

    >>> type(0b11), 0b11.bit_length()
    (<class 'int'>, 2)
    >>> 0b11, 0o11, 0x11
    (3, 9, 17)
    >>> 0b1010, 0xa, 0b010010, 0x12
    (10, 10, 18, 18)

Since 2, 8, and 16 are all powers of 2, while 10 is not, these three alternate number systems
can sometimes be useful for expressing values in a computer-friendly manner.

**Unicode** can be considered as a huge ASCII table, one with 1,114,112 possible code points.
(up to or 0x10ffff hexadecimal). The first 128 characters in the Unicode table correspond
to the ASCII characters, then e.g. `chr(2323)` returns `ओ`. Unicode itself is not an encoding.
and is better thought of as a map between characters (like "a", "¢" and "ओ") and distinct
positive integers.

Unicode doesn’t tell you how to convert text to binary data and vice versa.
This is where UTF-8 and other encoding schemes are involved.

**Encoding and Decoding**

    >>> 'hello'.encode('utf-8'), "résumé".encode("utf-8")
    (b'hello', b'r\xc3\xa9sum\xc3\xa9')

The results of `str.encode()` is a bytes object. Both bytes literals
(such as b"r\xc3\xa9sum\xc3\xa9") and the representations of bytes
permit only ASCII characters. `str.decode()` carriers out the reverse operation.
The encoding parameter is "utf-8" by default, but is often passed to be explicit.

All text (`str`) is Unicode by default and Python source code is assumed to be UTF-8 by default.
So all literal Unicode characters, e.g. "Δv / Δt", will be stored as Unicode.
A crucial feature is that UTF-8 is a variable-length encoding.

    >>> all(len(chr(i).encode("ascii")) == 1 for i in range(128))
    True

The length of a single Unicode character as a Python str will always be 1,
the length of the same character encoded to bytes will be anywhere between 1 and 4.

There are various built-in functions that relate to numbering systems and character encoding
`ascii()`, `bin()`, `hex()`, and `oct()` are for obtaining a different representation
of an input. Each one produces a str. The first, `ascii()`, produces an ASCII only
representation of an object, with non-ASCII characters escaped. The remaining three
give binary, hexadecimal, and octal representations of an integer.
`bytes()`, `str()`, and `int()` are class constructors for their respective types and each offer
a way to coerce the input into the desired type.
`ord()` converts a str character to its base-10 code point, while `chr()` does the opposite.

There are up to six ways you can type the same Unicode character,
as described in the Python [docs](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals)
on byte and string literals and the various escape sequences. "\uxxxx" can
be used to express a character with a 16-bit hex value xxxx, e.g. "\u0061" represents 'a'.

Care should be taken when using binary data (bytes) from an external source,
to check that the data specifies an encoding. E.g. latin encoding is required
in this line: `b"\xbc cup of flour".decode('latin')` otherwise `UnicodeDecodeError` will be raised.


String formatting
-----------------
See also notes on f-strings in [new features](/new-features).
While other string literals always have a constant value, formatted strings
are really expressions evaluated at run time.
Expressions in formatted string literals are treated like regular Python expressions
surrounded by parentheses, with a few exceptions, e.g. a lambda expression must be
surrounded by parentheses.

As stated in the [docs](https://docs.python.org/3/reference/lexical_analysis.html#f-strings),
if a conversion is specified, the result of evaluating
the expression is converted before formatting. Conversion `'!s'` calls `str()` on
the result, `'!r'` calls `repr()`, and `'!a'` calls `ascii()`:

    >>> name = "Fred"
    >>> f"He said his name is {name!r}."
    "He said his name is 'Fred'."
    >>> f"He said his name is {name}."
    'He said his name is Fred.'

Formatting a floating point number to a certain precision can be done as follows:

    >>> numvar = 4.625
    >>> f'{numvar:.6f}'
    '4.625000'

    >>> width = 10
    >>> precision = 4
    >>> value = decimal.Decimal("12.34567")
    >>> f"result: {value:{width}.{precision}}"  # nested fields
    'result:      12.35'

Misc. String methods
--------------------

`str.endswith` and `str.startswith` have optional start and end parameters, which allows
thecomparison to be restricted to a substring, e.g. `'foobar'.endswith('oob', 0, 4)  # True`

`str.center(<width>[, <fill>])` centers a string within a field, e.g. `'foo'.center(10)  # '   foo    '`,
`'bar'.center(10, '-')  # '---bar----'`. `str.rjust(<width>[, <fill>])`
right-justifies a string in a field e.g. `'foo'.rjust(10)  # '       foo'`

`str.partition(<sep>)` splits a string at the first occurrence of string `<sep>`.
`'foo.bar.foo.bar'.partition('.')  # ('foo', '.', 'bar.foo.bar')`. `str.rpartition()`
splits at the last occurrence.

