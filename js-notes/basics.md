
Difference between `==` and `===` is that `==` will perform a type convserion
when comparing objects whereas `===` will not.

Standard built-in objects
-------------------------
Here, global objects refer to objects in the global scope. The global scope consists of the properties of the global object (accessed using the `this` operator in the global scope), including inherited properties, if any.
Other objects in the global scope are either created by the user script or provided by the host application.

Value properties are global properties that return a simple value; they have no properties or methods. E.g. `NaN`, `undefined`, `null`

Function properties are functions which are called globally rather than on an object, e.g. `isNaN()`, `parseFloat()`, `parseInt()`

Fundamental objects are basic objects upon which all other objects are based, e.g. `Object`, `Function`, `Boolean`, `Error`

Numbers and dates: `Number`, `Math`, `Date`. Text processing: 'String', `RegExp`. Indexed collections: e.g. `Array`. Structured data e.g. `JSON`.

Keywords
--------
`let` allows you to declare variables that are limited in scope to the block, statement, or expression on which it is used. This is unlike the var keyword, which defines a variable globally, or locally to an entire function regardless of block scope.

    function letTest() {
      let x = 1;
      if (true) {
        let x = 2;  // different variable
        console.log(x);  // 2
      }
      console.log(x);  // 1
    }

Constants are block-scoped, much like variables defined using the let statement. The value of a constant cannot change through re-assignment, and it can't be redeclared.

    const number = 42;

    try {
      number = 99;
    } catch(err) {
      console.log(err);
      // expected output: TypeError: invalid assignment to const `number'
      // Note - error messages will vary depending on browser
    }

    console.log(number);
    // expected output: 42

Conditional statements: expressions and operators
-------------------------------------------------
    var a = 3;
    var b = -2;

    console.log(a > 0 && b > 0);
    // expected output: false

    console.log(a > 0 || b > 0);
    // expected output: true

    console.log(!(a > 0 || b > 0));
    // expected output: false

`switch` is a type of conditional statement that will evaluate an expression against multiple possible cases and execute one or more blocks of code based on matching cases. The switch statement is closely related to a conditional statement containing many else if blocks, and they can often be used interchangeably.

    switch (expression) {
        case x:
            // execute case x code block
            break;
        case y:
            // execute case y code block
            break;
        default:
            // execute default code block
    }

**The conditional operator**

    condition ? expr1 : expr2

If condition is true, the operator returns the value of expr1; otherwise, it returns the value of expr2. Used as a shortcut for the if statement.

    var age = 26;
    var canDrinkAlcohol = (age > 21) ? "True, over 21" : "False, under 21";
    console.log(canDrinkAlcohol); // "True, over 21"

Objects
-------
There are two ways to construct an object in JavaScript:
The object literal, which uses curly brackets: `{}`
The object constructor, which uses the `new` keyword

    // Initialize object literal with curly brackets
    const objectLiteral = {};

    // Initialize object constructor with new Object
    const objectConstructor = new Object();

    // Initialize gimli object
    const gimli = {
        name: "Gimli",
        race: "dwarf",
        weapon: "axe",
        greet: function() {
            return `Hi, my name is ${this.name}!`;
        },
    };

Sending gimli to the console will print out the entire object.

    gimli;
    // {name: "Gimli", race: "dwarf", weapon: "axe", greet: ƒ}

There are two ways to access an object's properties:
Dot notation and bracket notation.  Dot notation is faster and more readable, but has more limitations. Bracket notation allows access to property names stored in a variable, and must be used if an object's property contains any sort of special character.

    // Add new age property to gimli
    gimli.age = 139;

    // Add new fight method to gimli
    gimli.fight = function() {
        return `Gimli attacks with an ${this.weapon}.`;
    }

Strings
-------
    "How are you?"[5]; // r
    "How are you?".charAt(5); // r
    "How are you?".indexOf("are"); // 4
    "How are you?".slice(8, 11); // "you"
    "How are you?".length; // 12
    "How are you?".toUpperCase();
    "How are you?".toLowerCase();
    const originalString = "How are you?";
    const splitString = originalString.split(" ");  [ 'How', 'are', 'you?' ]
    const tooMuchWhitespace = "     How are you?     ";
    const trimmed = tooMuchWhitespace.trim(); // How are you
    const newString = originalString.replace("How", "Where");
    const favePoem = "My favorite poem is " + poem + " by " + author ".";
    const poem = "The Wide Ocean";
    const author = "Pablo Neruda";
    const favePoem = `My favorite poem is ${poem} by ${author}.`;

Arrays
------
There are two ways to create an array in JavaScript:
The array literal, which uses square brackets.
The array constructor, which uses the `new` keyword.

    // Initialize array of shark species with array constructor
    let sharks = new Array(
        "Hammerhead",
        "Great White",
        "Tiger",
    );

Classes
-------
A JavaScript class is a type of function. Classes are declared with the class keyword. We will use function expression syntax to initialize a function and class expression syntax to initialize a class.

    // Initializing a function with a function expression
    const x = function() {}
    // Initializing a class with a class expression
    const y = class {}

A constructor function is initialized with a number of parameters, which would be assigned as properties of this, referring to the function itself. The first letter of the identifier would be capitalized by convention.

    // Initializing a constructor function
    function Hero(name, level) {
        this.name = name;
        this.level = level;
    }

When we translate this to the class syntax, shown below, we see that it is structured very similarly.
The only difference in the syntax of the initialization is using the class keyword instead of function, and assigning the properties inside a constructor() method.

    // Initializing a class definition
    class Hero {
        constructor(name, level) {
            this.name = name;
            this.level = level;
        }
    }

Iteration
---------
    const popLimit = 10;

    // Start off with 0 fish
    let fish = 0;

    // Initiate while loop to run until fish reaches population limit
    while (fish < popLimit) {
        // add one fish for each iteration
        fish++;
        console.log("There's room for " + (popLimit - fish) + " more fish.");
    }

Here we set our while loop to run as long as the number of fish was less than the population limit of the aquarium. For each iteration, one fish is added to the aquarium until all 10 spots are filled. At that point, the loop stops running.

    let shellfish = [
        "oyster",
        "shrimp",
        "clam",
        "mussel",
    ];

Equivalent to for loop, print each item in Python:

    // Loop through each mammal
    for (let mammal of mammals) {
        console.log(mammal);
    }

Equivalent to enumerate in Python:

    // Loop through the length of the array
    for (let i = 0; i < shellfish.length; i++) {
      console.log(i, shellfish[i]);
    }

JSON
----
Developed to be compatible with any programming language.

    var user = {
    first_name: "Sammy",
    last_name : "Shark",
    online    : true,
    full_name : function() {
       return this.first_name + " " + this.last_name;
       }
    };

While similar, the above object differs from JSON in that keys in the object
are not enclosed by quotes, and also since it contains a function.

    var obj = {"first_name" : "Sammy", "last_name" : "Shark", "location" : "Ocean"}
    obj.first_name //Sammy
    var s = JSON.stringify(obj)   // '{"first_name" : "Sammy", ..
    var o = JSON.parse(s)

Converting JSON to sring is useful for transporting data from a client to a server in a lightweight way.
to convert them back to a JSON object on the client and/or the server side use `JSON.parse()`

    <!DOCTYPE html>
    <html>
    <body>

    <p id="user"></p>

    <script>
    var s = '{"first_name" : "Sammy", "last_name" : "Shark", "location" : "Ocean"}';

    var obj = JSON.parse(s);

    document.getElementById("user").innerHTML =
    "Name: " + obj.first_name + " " + obj.last_name + "<br>" +
    "Location: " + obj.location;
    </script>

    </body>
    </html>

Arrow Functions
---------------
An arrow function expression has a shorter syntax than a function expression and does not have its own this, arguments, super, or new.target.
Arrow functions do not have their own arguments object. Thus, in this example, arguments is simply a reference to the arguments of the enclosing scope:

    var arguments = [1, 2, 3];
    var arr = () => arguments[0];

    arr(); // 1

    function foo(n) {
      var f = () => arguments[0] + n; // foo's implicit arguments binding. arguments[0] is n
      return f();
    }

    foo(3); // 6


