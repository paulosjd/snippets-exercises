**Functional class pattern**

    function User(name, birthday) {
      // only visible from other methods inside User
      function calcAge() {
        return new Date().getFullYear() - birthday.getFullYear();
      }
      this.sayHi = function() {
        alert(`${name}, age:${calcAge()}`);
      };
    }

    let user = new User("John", new Date(2000, 0, 1));
    user.sayHi(); // John, age:17

In this code variables `name`, `birthday` and the function `calcAge()` are internal, private to the object. They are only visible from inside of it.

On the other hand, `sayHi` is the external, public method. The external code that creates user can access it.

This way we can hide internal implementation details and helper methods from the outer code. Only what’s assigned to `this` becomes visible outside.

**Factory class pattern**

We can create a class without using new at all:

    function User(name, birthday) {
      // only visible from other methods inside User
      function calcAge() {
        return new Date().getFullYear() - birthday.getFullYear();
      }

      return {
        sayHi() {
          alert(`${name}, age:${calcAge()}`);
        }
      };
    }

    let user = User("John", new Date(2000, 0, 1));
    user.sayHi(); // John, age:17



