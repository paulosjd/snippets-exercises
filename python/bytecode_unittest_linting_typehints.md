

As Python is dynamically typed, the interpreter only does type checking as code runs, so the
following does not raise a `TypeError`:

    >>> print(1 + 'two' if False else 3)  # 3

Recent versions of Python allow you to specify explicit type hints that can be used by different
tools to help in code development. Advantages of adding types:

-  Type checking with a tool like [mypy](http://mypy-lang.org) allows you to pick up errors,
for example a function called with an argument of the wrong type

- Type hints improve IDEs and linters. By allowing static reasoning of code, IDEs are able
to give better code completion, and provide warnings if an incorrect type is being passed.

Type hinting adds a lot of value for libraries used by others. It is also useful for
large projects to show how types flow through the code and to provide documentation.
For short throw-away scripts they add little value.

A type checker is expected to check the body of a checked function for consistency with the given
annotations. The annotations may also used to check correctness of calls appearing in other
checked functions.

Usage example: hearts card game [source code](https://github.com/paulosjd/misc-python-scripts/blob/master/type_hinting_hearts.py).

PEP 484 -- Type Hints
---------------------

[PEP 484](https://www.python.org/dev/peps/pep-0484) provides standard definitions and tools for
static type analysis. The following functions argument and return type are declared in the annotations:

    def greeting(name: str) -> str:
        return 'Hello ' + name

Note that no type hints have no effect at runtime. Instead,
existence of a separate off-line type checker is assumed, which users can run over their source code
voluntarily and use as a very powerful linter.

**Acceptable type hints**

Type hints may be built-in classes from the standard library, types available in the `types` module, and user-defined classes.
In addition to the above, the following special constructs defined below may be used: `None`, `Any`,
`Union`, `Tuple`, `Callable` (for frameworks expecting callback functions of specific signatures),
all ABCs and stand-ins for concrete classes exported from `typing` (e.g. `Sequence` and `Dict`).

    def example(my_flag: bool = False) -> List[Tuple[str, str]]:
        ...

If it doesn't matter whether what kind of sequence it is,
a `Sequence` is anything that supports `len()` and `.__getitem__()`:

    from typing import List, Sequence

    def square(elems: Sequence[float]) -> List[float]:
        return [x**2 for x in elems]

If you use `Any`, the static type checker will effectively not do any type any checking.
But this does allow you to gradually add type hints to your code.

[Further reading](https://www.python.org/dev/peps/pep-0484/#id49) on the `typing` module and its fundamental building blocks.

Annotations should be kept simple or static analysis tools may not be able to interpret the values.
Dynamically computed types are unlikely to be understood.
While annotations are normally the best format for type hints, sometimes it is more
appropriate to represent them by a special comment, or in a separately distributed stub file.
Note that the return type of `__init__` should be annotated with `-> None`.

**Type Aliases**

Useful for making your code more readable and its intent clearer.

    from typing import List, Tuple

    Card = Tuple[str, str]
    Deck = List[Card]

    def deal_hands(deck: Deck) -> Tuple[Deck, Deck, Deck, Deck]:
        """Deal the cards in the deck into four hands"""
        return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])

Anything that is acceptable as a type hint is acceptable in a type alias:

    from typing import TypeVar, Iterable, Tuple

    T = TypeVar('T', int, float, complex)
    Vector = Iterable[Tuple[T, T]]

    def inproduct(v: Vector[T]) -> T:
        return sum(x*y for x, y in v)

Further example of a type variable, this time acceptable types are `str` and `float`:

    Choosable = TypeVar("Choosable", str, float)

    def choose(items: Sequence[Choosable]) -> Choosable:
        return random.choice(items)

**Forward references**

When a type hint contains names that have not been defined yet,
that definition may be expressed as a string literal, to be resolved later.

A common use for forward references is when e.g. Django models are needed in the signatures.
The following avoids circular imports:

    # File models/a.py
    from models import b
    class A(Model):
        def foo(self, b: 'b.B'): ...

    # File models/b.py
    from models import a
    class B(Model):
        def bar(self, a: 'a.A'): ...

**Union types**

Since accepting a small, limited set of expected types for a single argument is common,

    from typing import Union

    def handle_employees(e: Union[Employee, Sequence[Employee]]) -> None:
        if isinstance(e, Employee):
            e = [e]
        ...

One common case of union types are *optional* types. By default, `None` is an invalid value for any type, unless a default value of `None` has been provided in the function definition. Examples:

    def handle_employee(e: Union[Employee, None]) -> None: ...

As a shorthand for `Union[T1, None]` you can write `Optional[T1]`; for example, the above is equivalent to:

    from typing import Optional

    def handle_employee(e: Optional[Employee]) -> None:
        ...

**Type Theory**

In talking about class objects that inherit from a given class: `Type[C]` where `C` is a class.
While `C` (when used as an annotation) refers to instances of class `C`, `Type[C]`
refers to subclasses of `C`.

Subtypes are somewhat related to subclasses. In fact all subclasses corresponds to subtypes,
and `bool` is a subtype of int because `bool` is a subclass of `int`.
However, there are also subtypes that do not correspond to subclasses. E.g. `int` is a subtype
of `float`, but `int` is not a subclass of `float`.

Consider `bool` and `int`. The `bool` type takes only two values, `True` and `False`, names that
are just aliases for the integer values `1` and `0`

    >>> True + True  # 2
    >>> issubclass(bool, int)  # True

The importance of subtypes is that a subtype can always pretend to be its supertype.
For instance, the following code type checks as correct:

    def double(number: int) -> int:
        return number * 2

    print(double(True))  # Passing in bool instead of int

**Annotating instance and class methods**

Usually the first argument of class and instance methods does not need to be annotated, but
can be annotated with a type variable. In this case the return type may
use the same type variable, thus making that method a generic function. For example:

    T = TypeVar('T', bound='Copyable')
    class Copyable:
        def copy(self: T) -> T:
            # return a copy of self

    class C(Copyable): ...
    c = C()
    c2 = c.copy()  # type here should be C

**using `Optional` for `None` default arguments**

The Optional type simply says that a variable either has the type specified or is None.
An equivalent way of specifying the same would be using the Union type: `Union[None, str]`

Note that the use of `None` for optional arguments is so common that `mypy` automatically
assumes that a default argument of `None` indicates an optional argument even with the type hint
explicitly saying so. So instead of having `start: Optional[str] = None` in the following example,
this would work:

    def player_order(names: Sequence[str], start: str = None) -> Sequence[str]:
        ...

**Stub Files**

Stub files are files containing type hints that are only for use by the type checker.
Use cases include extension modules, third-party and standard library modules whose authors
have not yet added type hints. E.g. we may be using a number of function from a module,
and so we would like the calls to them to be type checked.

The type checker should only check function signatures in stub files.
No runtime behavior is expected of these .pyi files, which are just there to provide the interfaces/call
signatures of the functions in the compiled module.
It is recommended that function bodies in stub files just be a single ellipsis (...).

The type checker should have a configurable search path for stub files.
While stub files are syntactically valid Python modules, they use the .pyi extension to make it
possible to maintain stub files in the same directory as the corresponding real module.

To set up, ut all your stub files inside one common directory, and set the `MYPYPATH` environment
variable to point to this directory as follows:

    $ export MYPYPATH=/home/gahjelle/python/stubs

You can set the variable permanently by adding the line to your `.bashrc file`.  Next, create a
file inside your stubs directory that you call `parse.pyi`. It must be named for the package that
you are adding type hints for, with a `.pyi` suffix.

Linting
-------

A linter is a program wjhich analyses you code, looking for errors.
It also is a style checker which enforces PEP 8, a type checker which looks for type errors ,
and a structural analyzer which looks for e.g. various design antipatterns  or bad implementations
of special methods. Additional advantages:

- Enforce a consistent coding standard across your project

- Ensure best practice and improve the general code quality of your projeect

Linting is particularly useful for big legacy systems with only few tests.
Even if test coverage is good it doesn't mean code is necessarily
safe so an extra layer of assurance is desirable.

Potential bugs can be picked up. E.g. show lines with unreachable code,
statements which seem to have no effect and unused variables and imports.

Other potential bugs picked up are undefined variables and calls to objects which
aren't callable. Also, constant `if` conditions, e.g. forgotten to call the function:

    $ cat a.py

    def func():
        return bool(some_condition)

    # func itself (not the return value) is always truthy
    if func:
        pass

    $ pylint a.py
    W: 5: Using a conditional statement with a constant value

Flake8 and Pylint are common tools. Flake8 is quick to set up and has a low rate of false positives
compared to Pylint which on the other hand provides a more comprehensive analysis.
By connecting one of these with a CI platform, you can enforce good code quality, catch potential bugs,
require proper documentation and PEP 8 compliance etc. In this way people responsible for code reivew
of a PR do not even need to look at it until the build passes.


Bytecode
---------
You want to write human-readable source code but your PC wants binary instructions (machine-code)
for its CPU. So:

- some languages compile directly to CPU instructions
- some interpret source code directly while running
- some compile to an intermediate set of instructions, and implement a virtual machine that
turns those into CPU instructions while running. That is bytecode.

Python (the CPython implementation) compiles to bytecode which runs on the Python VM.
.pyc files can be found in the `__pycache__` directory.
and these contain the compiled bytecode. This means source code does not need to be re-parsed every time it runs.
Suppose you typed the following function into a Python interpreter:

    >>> def myfunc():
        return 6 / 2
    >>> myfunc.__code__.co_consts
    (None, 6, 2)
    >>> myfunc.__code__.co_code
    'd\x01\x00d\x02\x00\x15S'

This code object contains everything needed to execute the function.
Code objects are the compiled representation of a piece of code. This representation
can then be understood by the cPython interpreter and executed line-by-line.

`co_consts` contains constants used by the function and `co_code` contains the
byte code instructions, generated by compiling the function. When represented as a string,
the byte code instructions does not make much sense. Printing it in hex:

    >>> for i, ch in enumerate(myfunc.__code__.co_code):
        print('{}: {}'.format(i, ch.encode('hex')))
    0: 64
    1: 01
    2: 00
    3: 64
    ...

The first byte code instruction is `0x64`. How do we determine what that actually means?
The `dis` module has a mapping for byte code instructions from opcodes to mnemonics.

    >>> import dis
    >>> print dis.opname[0x64]
    LOAD_CONST

The first instruction in the byte code string, is `LOAD_CONST`. The instruction is followed
by 2 byte integer operand. The operand is an index into the `co_const` tuple that
specifies the constant to be pushed / loaded into the stack. The operand specified
in this case is `0x0001`, which corresponds to the constant `6`. Another example:

    def hello()
        print("Hello, World!")
This is the bytecode it turns into (translated into a human-readable form):

    2           0 LOAD_GLOBAL              0 (print)
                2 LOAD_CONST               1 ('Hello, World!')
                4 CALL_FUNCTION            1

**Inside the Python virtual machine**

CPython uses a stack-based virtual machine. That is, it's oriented entirely around
stack data structures (where you can "push" an item onto the "top" of the structure, or
"pop" an item off the "top").

CPython uses three types of stacks:

1) The call stack. This is the main structure of a running Python program. It has one item,
a "frame" for each currently active function call.
Every function call pushes a new frame onto the call stack, and every time a function
call returns, its frame is popped off.

2) In each frame, there's an evaluation stack (data stack),
where execution of a Python function occurs. Executing bytecode instructions consists mostly of
pushing things onto this stack, manipulating them, and popping them back off.

3) Also in each frame, there's a block stack, used by Python to keep track of certain types
of control structures: loops, `try`/`except` blocks, and `with` blocks all cause entries
to be pushed onto the block stack, and the block stack gets popped whenever you exit
one of those structures.

Suppose we have some code that calls a function, like this: `my_function(my_variable, 2)`.
Python will translate this into a sequence of four bytecode instructions:

1) A `LOAD_NAME` instruction that looks up the function object `my_function` and pushes it onto the top of the evaluation stack
    Another `LOAD_NAME` instruction to look up the variable `my_variable` and push it on top of the evaluation stack
    A `LOAD_CONST` instruction to push the literal integer value `2` on top of the evaluation stack
    A `CALL_FUNCTION` instruction

The `CALL_FUNCTION` instruction will have an argument of `2`, which indicates that Python
needs to pop two positional arguments off the top of the stack; then the function to call
will be on top, and it can be popped as well. Then a new frame will be allocated on the call stack,
populate the local variables for the function call, and execute the bytecode of `my_function`
inside that frame. Then, the frame will be popped off the call stack,
and in the original frame the return value of `my_function` will be pushed on top of the
evaluation stack.

**Accessing and understanding Python bytecode**

the `dis` module provides a "disassembler" for Python bytecode, making it easy to get a
human-readable version and look up the various bytecode instructions.
The function `dis.dis()` will disassemble a function, method, class, module, compiled
Python code object, or string literal containing source code and print a human-readable version.

Anticipating what bytecode your source code turns into can help you make better
decisions about how to write and optimize it. It will help you understand why
certain constructs are faster than others. For instance, `{}` is faster than `dict()`, which can
be understood by comparing the output of `dis.dis("{}")` with `dis.dis("dict()")`.

Unit testing
------------

"Debugging is hard, testing is easy". Unit tests verify that the code behaves as expected,
saving time in the long run and making development more predictable.
It often leads to better design. If you try to write a test and it is really difficult,
or you realize that it interacts with a lot of components in your system,
that is a sign that you may not have  designed that unit of code the best way you could.
Also it gives you the confidence to work on code without fear of breaking
existing functionality. This is especially helpful when refactoring code.

FIRST testing principles: fast, informative (tell you where the failure occurred), repeatable,
self-verifying, timely (if tests written long after code is written then you lose some benefits
e.g. better design).

Unit tests do not prove that code is correct, just that the
code behaves as expected.
Unit testing is much easier with code that is loosely coupled.
Code which isolates external resources can easily
replace them in testing with mock objects.
Applications designed to be easily testable tend towards being more modular
and having looser coupling of components.

**Mocking**

The core logic of units of code should be tested in isolation from external code or services they depend upon,
e.g. by mocking interactions to the outside world.
Mocks allow you to control the behavior of code during testing.
Replacing actual HTTP requests, for example, with a mock object allows the simulation of
external service outages and successful responses in a predictable way.
Also, certain lines of code, e.g. within `except` blocks and `if` statements, can be hard to
test without using mock objects which enable the execution path of the code to be controlled.

`patch()` from `unittest.mock` is used as a decorator or a context manager and will
look up an object in a given module and replace that object with a `Mock`.

[](./images/patch1.png)

Example of mocking a system call:

    def delete_file(full_path_to_file):
        if os.path.isfile(full_path_to_file):
            os.remove(full_path_to_file)

     @mock.patch(‘fs_handler_main.os.path.isfile’)
     @mock.patch(‘fs_handler_main.os.remove’)
     def test_delete_file_success(self, mock_os_remove, mock_os_is_file):
         mock_os_is_file.return_value = True
         delete_file(self.full_path)
         mock_os_remove.assert_called_with(self.full_path)

`patch.object()`

This takes the same configuration parameters that `patch()` does but instead
of passing the target’s path, you pass the target object itself as the first parameter.
In the follwing example, `get()` is mocked. Every other attribute remains the same.

    from my_calendar import requests, get_holidays

    class TestCalendar(unittest.TestCase):
        @patch.object(requests, 'get', side_effect=requests.exceptions.Timeout)
        def test_get_holidays_timeout(self, mock_requests):
                with self.assertRaises(requests.exceptions.Timeout):
                    get_holidays()

`side_effect` is useful to configure mock objects, not only for raising
exceptions to test error handling, but also where your mock is going to
be called several times, and you want each call to return a different value.

Another benefit of using mock objects is that is enables you to test
how you’re using their real counterparts in your code
`Mock` instances store data on how you used them and it is desirable in many cases to test
if and how many times a mocked callable is called, as well as the call arguments.
Assertion functions and attributes such as `.assert_called()`, `.assert_called_with()`,
`call_args`, `call_count` are useful in this regard.

A potential issue with mocking: tests *not* breaking after changes to external dependencies
On one hand, mocking code that makes a request helps you to test components
in isolation under controlled conditions. However, it also presents a potential problem.
If an external dependency changes its interface then your Python mock objects become invalid.
It may be that your tests will pass because your mock objects have masked
the change, but your production code will fail.

**Libraries for fixtures**

[FactoryBoy](https://factoryboy.readthedocs.io/en/latest/introduction.html)
and [Faker](https://faker.readthedocs.io/en/latest/)
are popular libraries for creating fixture data.
Compared to e.g. preparing your test data by using Django ORM directly,
factories and `factory_boy` specifically have several advantages:

 - your model factories are defined in a nice, clean and readable manner,
  whose class-based approach allows for inheritance as well as the creation of
  [SubFactories](https://factoryboy.readthedocs.io/en/latest/reference.html#subfactory)

- `Sequence`s which help make the data more "dynamic".

- `factory_boy` is there to avoid writing "helper" functions for generating
test data, i.e. reinventing. Instead, it introduces a nice and easy-to-use
interface.

The purpose of `factory_boy` is to provide a default way of getting a
new instance, while still being able to override some fields on a per-call basis.

Factories declare a set of attributes used to instantiate an object,e.g.
its model attribute to the target class and defaults for keyword args to
pass to the associated class’ `__init__` method).

    class UserFactory(factory.Factory):
        class Meta:
            model = base.User

        firstname = "John"
        lastname = "Doe"
        username = factory.Sequence(lambda n: 'user%d' % n)

    >>> jack = UserFactory(firstname="Jack")
    <User: Jack Doe>

Sequences are useful when a field has a unique key and so each object
generated by the factory should have a different value for that field.

***

For Django there is the `DjangoModelFactory` class and a
`mute_signals` decorator for when you don't want a signal to be dispatched in testing.

    class AccountFactory(factory.django.DjangoModelFactory):
        FACTORY_FOR = Account
        user = factory.SubFactory('app.factories.UserFactory')
        currency             = 'USD'
        balance              = '50.00'

    class UserFactory(factory.django.DjangoModelFactory):
        FACTORY_FOR = User
        username = factory.Sequence(lambda n : "bob {}".format(n))

***

Use `faker.Faker()` to create and initialize a faker generator, which can
generate data by accessing properties named after the type of data you want:

    from faker import Faker
    fake = Faker()

    fake.name()
    # 'Lucy Cechtelar'

    fake.address()
    # '426 Jordy Lodge
    #  Cartwrightshire, SC 88120-6700'

    fake.text()
    # 'Sint velit eveniet. Rerum atque repellat voluptatem quia rerum. Numquam excepturi
    #  beatae sint laudantium

    for _ in range(3):
      print(fake.name())

    # 'Adaline Reichel'
    # 'Dr. Santa Prosacco DVM'
    # 'Noemy Vandervort V'

When using Faker for unit testing, you will often want to generate the
same data set. Calling the same methods
with the same version of faker and seed produces the same results:

    fake = Faker()
    fake.seed(4321)

    print(fake.name())
    # 'Margaret Boehm'

    fake = Faker()
    fake.seed_instance(4321)

    print(fake.name())
    # 'Margaret Boehm'

File system tasks
-----------------

Modules with functions for handling files include  `os`, `os.path`, `shutil`, and `pathlib`.
The `pathlib` module was introduced in Python 3.4
([PEP 428](https://www.python.org/dev/peps/pep-0428/)) to deal with the slightly
cumbersome nature of often needing to use different functionality spread across
the standard library (in `os`, `glob`, and `shutil`).
It gathers this functionality in one place on a `Path` object.
It is also more consistent across different OS's.
`pathlib.Path` class methods `.cwd()` and `.home()`:

    >>> pathlib.Path.cwd()
    PosixPath('/home/pauljd/mydir/')

    >>> pathlib.Path.home().joinpath('python', 'scripts', 'test.py')
    PosixPath('/home/pauljd/mydir/scripts/test.py')

The `open()` function can use `Path` objects directly:

    path = pathlib.Path.cwd() / 'test.md'
    with open(path, mode='r') as fid:
        headers = [line.strip() for line in fid if line.startswith('#')]
    print('\n'.join(headers))

But an equivalent is to call `.open()` on the `Path` object (which calls the built-in `open()` behind the scenes):

    with path.open(mode='r') as fid:
        ...

**Directory listing**

The following lists all files in a directory using `os.scandir()`, which
implements the [context manager](/context-managers) protocol:

    with os.scandir('my_directory/') as entries:
        for entry in entries:
            if entry.is_file():
                print(entry.name)

A similar thing can be done using `pathlib.Path()` e.g. `[f.name for f in Path('my_directory/').iterdir() if f.is_file()]`.
To list subdirectories instead of files, call `.is_dir()` on each entry instead of `.is_file()`.

Entries returned by these iterators also have methods such as
`.stat()`, that retrieves information about the file or directory

**Making directories**

Making directories can be done using `os.mkdir('example_directory/')`
or `Path('example_directory/').mkdir()`. A `FileExistsError` is raised if
the directory already exists. This can be caught in a `try`/`except` block,
or it can be ignored by passing the `exist_ok=True` argument to `.mkdir()`.

**Filename Pattern Matching**

After getting a list of files in a directory using one of the above methods,
you can search for files that match a particular pattern using the following:

- string methods, for example: `[f.name for f in Path('my_directory/').iterdir() if f.endswith(.txt)]`

- `fnmatch.fnmatch()`, for example:
`[f.name for f in Path('my_directory/').iterdir() if fnmatch.fnmatch(filename, 'data_*_backup.txt')]`

- `glob.glob()` returns a list of filenames that match a pattern

- `pathlib.Path.glob()` finds patterns in path names and returns a generator object

Translating name patterns with wildcards like `?` and `*` into a list of
files is called globbing. E.g.  typing `mv *.py python_files/` moves all files.
`glob` supports shell-style wildcards to match patterns
as well as searching for files recursively in subdirectories (`.iglob()` returns an iterator instead of a list):

    [name for name in glob.glob('*[0-9]*.txt')]
    [name for name in glob.iglob('**/*.py', recursive=True)]
    [name for name in Path('.').glob('*.p*')]

**Walking a directory tree and processing files: `os.walk()`**

`os.walk()` is used to generate filename in a directory tree by walking
the tree either top-down (by default) or bottom-up.
This is useful for e.g. recursively deleting files and directories.
The following lists all files and directories in a directory tree:

    for dirpath, dirnames, files in os.walk('.'):
        print(f'Found directory: {dirpath}')
        for file_name in files:
            print(file_name)

**Temporary Files and Directories**

The `tempfile` module can be used to open and store temp data in
a file or directory while your program is running.
In the following example, the mode is 'w+t', to
create a temp text file in write mode.
`tempfile.TemporaryFile()` implements the [context manager](/context-managers)
protocol, so can be used in a `with` statement which takes care of closing and deleting the
file after it has been read:

    with TemporaryFile('w+t') as fp:
        fp.write('Hello universe!')
        fp.seek(0)
        fp.read()
    # File is now closed and removed

Once the file is closed, it will be deleted from the filesystem.
`tempfile.NamedTemporaryFile` can be used if a named temp file is needed.
`tempfile.TemporaryDirectory` works in a similar way to the above.

**Deleting Files and Directories**

To delete a single file, use `pathlib.Path.unlink()`, `os.remove()`
or `os.unlink()`:

    data_file = 'home/data.txt'
    # If the file exists, delete it
    if os.path.isfile(data_file):
        os.remove(data_file)

To delete an empty directory, use `os.rmdir()` or `pathlib.rmdir()`.
To delete non-empty ones, use `shutil.rmtree()`.

    trash_dir = Path('my_documents/empty_dir')
    trash_dir.rmdir()
    os.rmdir('desktop/empty_dir')
    shutil.rmtree('desktop/non_empty_dir')

**Shell utilities: `shutil`**

`shutil.copy()` is comparable to the `cp` shell command,
`shutil.copytree()` is like with `-r`.
To move a file or directory, use `shutil.move(src, dst)`.
