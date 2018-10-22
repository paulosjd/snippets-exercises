The idea is to solve a subproblem that is a smaller instance of the same problem, and then use the solution to that smaller instance to solve the original problem.

A factorial is the product of the integers 1 through to *n*. For example, 5! equals 1 x 2 x 3 x 4 x 5

    1 x 2 x 3 x 4 x 5
    1 x 2 x 3 x 4
    1 x 2 x 3
    1 x 2
    1
    ((((1 x (1 x 2)) x 3) x 4) x 5)

We solved the problem of computing n! (the original problem) by solving the subproblem of computing the factorial of a smaller number (n−1)! and then using the solution to the subproblem to compute the value of n!

    def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

Recursive list sum. 4 + (3 + (2 + (1))):

    def sum_list(n):
        if n == 0:
            return 0
        else:
            return n + sum_list(n-1)

We can distill the idea of recursion into two simple rules:

1) Each recursive call should be on a smaller instance of the same problem, that is, a smaller subproblem.

2) The recursive calls must eventually reach a base case, which is solved without further recursion.

E.g. analogous example to factorial, problem is broken down into smaller problems (function calling itself with `n - 1`) until no further recursion possible, the terminating condition, which is `if n == 0`,   4 + (3 + (2 + (1)))

    def sum_list(n):
        if n == 0:
            return 0
        return n + sum_list(n-1)

Another example is a test to see whether a word is a palindrome (without checking if `word == word[::-1]`).
Involves keep stripping off and testing the first and last characters:

    def is_palindrome(word):
        if word[0] != word[-1]:
            return False
        try:
            return is_palindrome(word[1:-1])
        except IndexError:
            return True

Pascal's triangle:

    def pascal(n):
        if n == 1:
            return [1]
        line = [1]
        previous_line = pascal(n - 1)
        inner = []
        if n > 3:
            inner = [previous_line[a] + previous_line[a + 1] for a in range(int(n / 2 - 1))]
            inner = inner + inner[::-1]
        for i in inner:
            line.append(i)
        if n % 2 != 0:
            ind = int(n / 2)
            line.insert(ind, previous_line[ind] + previous_line[ind - 1])
        line.append(1)
        return line

*See also*: Trees in data_structures.md