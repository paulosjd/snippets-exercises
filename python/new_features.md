Data classes
------------
[Dataclasses](https://docs.python.org/3/library/dataclasses.html) typically containing mainly
just data and are created using the `@dataclass` decorator. Although they use a very different
mechanism, data classes can be thought of as "mutable namedtuples with defaults".

The `dataclass()` decorator inspects a class definition for variables with type annotations
as defined in PEP 526. For example, this code:

    @dataclass
    class InventoryItem:
        '''Class for keeping track of an item in inventory.'''
        name: str
        unit_price: float
        quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

Will add, among other things, a `__init__()` that looks like:

    def __init__(self, name: str, unit_price: float, quantity_on_hand: int=0):
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand

Note that this method is automatically added to the class, along with methods
such as `__repr_()` and `__eq__()` which give basic functionlity such as object comparisons
and string representations. Since a data class is just a regular class, you can add methods
as you would do normally.

While similar to a `namedtuple` in many respects, data classes do not have the limitations
of being hard to add default values to, and also that they are immutable. So common use
cases are where you would normally use a `namedtuple` but want to avoid these limitations.
One main design goal of dataclasses is to support static type
checkers ([type hinting notes](./type-hinting)); they support typing out of the box.

Using the `dataclass()` decorator makes it quick and easy to write robust classes,
in particular small classes that mainly store data.
They reduce boilerplate code since special methods are automatically added. In the following example:

    from dataclasses import dataclass, field

    @dataclass(order=True)
    class Country:
        name: str
        population: int
        area: float = field(repr=False, compare=False)
        coastline: float = 0

        def beach_per_person(self):
            """Meters of coastline per person"""
            return (self.coastline * 1000) / self.population

You can use the `Country` data class like any other class (including e.g. inheritance):

    >>> norway = Country("Norway", 5320045, 323802, 58133)
    >>> norway
    Country(name='Norway', population=5320045, coastline=58133)

    >>> nepal = Country("Nepal", 29384297, 147181)
    >>> nepal
    Country(name='Nepal', population=29384297, coastline=0)

    >>> norway == norway, norway == nepal
    (True, False)

    >>> sorted((norway, nepal))
    [Country(name='Nepal', population=29384297, coastline=0),
     Country(name='Norway', population=5320045, coastline=58133)]

A custom `repr` could be defined the same as for regular classes.
Above, the `.area` field was left out of the `repr` and the comparisons.
By default, data classes can be compared for equality. Since `order=True`
is specified in the decorator, the `Country` class can also be sorted.
The sorting is on the field values, using `.name` then `.population`, and so on,
but this can be customized using `field()`.

Built-in function: `breakpoint()`
----------------------------------
Drops you into the debugger at the call site. In most cases,
it is purely a convenience function so you don’t have to explicitly
import `pdb` and type as much.

As explained in PEP 553 [Rationale](https://www.python.org/dev/peps/pep-0553/#id9),
the idiom `import pdb; pdb.set_trace()` has disadvantages in that it is long to
type and is easy to make a typo, it ties debugging directly to the choice of pdb instead
of IDE options, and linters complain about this line because it contains two statements
(to avoid mistakes at cleanup time).

By default, `sys.breakpointhook()` implements the actual importing and
entry into `pdb.set_trace()`, and it can be set to a different function to
change the debugger that `breakpoint()` enters.

The default implementation of `sys.breakpointhook()` consults a new
environment variable called `PYTHONBREAKPOINT`. This environment variable
can have various values, allowing external processes to control how
breakpoints are handled. E.g. disabling accidental `breakpoint()` calls pushed
to production, or IDEs which run the program in its debugging
environment with `PYTHONBREAKPOINT` set to their internal debugging hook.

Assignment Expresssions
-----------------------

Current:

    env_base = os.environ.get("PYTHONUSERBASE", None)
    if env_base:
        return env_base

Improved:

    if env_base := os.environ.get("PYTHONUSERBASE", None):
        return env_base

There is new syntax (the “walrus operator”, `:=`) to assign values to
variables as part of an expression. E.g.:

    if (n := len(a)) > 10:
        print(f"List is too long ({n} elements, expected <= 10)")

The rationale for [PEP 572](https://www.python.org/dev/peps/pep-0572/)
is that some code could have been written clearer with (sparing) use of
assignment expressions.
Programmers may value writing fewer lines over shorter lines and Guido
found several examples where a programmer repeated a subexpression,
slowing down the program, in order to save one line of code, e.g. instead
of writing:

    match = re.match(data)
    group = match.group(1) if match else None

they would write:

    group = re.match(data).group(1) if re.match(data) else None

The same things may occur in saving an extra level of indentation.

**Examples**

    # Handle a matched regex
    if (match := pattern.search(data)) is not None:
        # Do something with match

    # Reuse a value that's expensive to compute
    [y := f(x), y**2, y**3]

    # Share a subexpression between a comprehension filter clause and its output
    filtered_data = [y for x in data if (y := f(x)) is not None]

    # Map and filter efficiently by capturing the condition
    results = [(x, y, x/y) for x in input_data if (y := f(x)) > 0]

    # Reuse a subexpression within the main expression
    stuff = [[y := f(x), x/y] for x in range(5)]
