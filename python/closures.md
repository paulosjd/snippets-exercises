    def bar(arg1):
        def inner_bar(f):
            def inner_inner_bar(*args, **kwargs):
                new_args = (x + arg1 for x in args)
                return f(*new_args, **kwargs)
            return inner_inner_bar
        return inner_bar

    @bar(4)
    def foo(x, y):
        print("Sum is {0}".format(x+y))

    >>> foo(3, 5)
    Sum is 16


**Javascript**

    function outerFunc(){
        var outerVar = 'an outerFunc var';
        return function(){
            alert(outerVar);
        }
    }

    outerFunc()(); //returns inner function and fires it

...when an inner function references an outer function's variables. With closures the vars referenced are maintained even after the outer function is done or 'closed'
Whereas the local variable in `outerFunc()` would normally be garbage collected after it is executed, closures have access to the variables they were created in.

A closure is a special kind of object that combines two things: a function, and the environment in which that function was created. The environment consists of any local variables that were in-scope at the time that the closure was created.
[MDN docs](https://developer.mozilla.org/en-US/docs/JavaScript/Guide/Closures)

A "closure" is an expression (typically a function) that can have free variables together with an environment that binds those variables (that "closes" the expression).

A simple explanation for closures:

    Take a function. Let's call it F.
    List all the variables of F.
    The variables may be of two types:
        Local variables (bound variables)
        Non-local variables (free variables)
    If F has no free variables then it cannot be a closure.
    If F has any free variables (which are defined in a parent scope of F) then:
        There must be only one parent scope of F to which a free variable is bound.
        If F is referenced from outside that parent scope, then it becomes a closure for that free variable.



