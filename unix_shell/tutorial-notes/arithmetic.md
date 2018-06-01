``let`` is a builtin function of Bash that allows us to do simple arithmetic.
 It can take a variety of formats following:
 
     let <arithmetic expression>
     
 The first part is generally always a variable which the result is saved
 into. Note that the first two expressions are the same but quotes are used in the second
 to make it more readable.
 
    #!/bin/bash
    let a=5+4
    echo $a # 9
    let "a = 5 + 4"
    echo $a # 9
    let a++
    echo $a # 10
    let "a = 4 * 5"
    echo $a # 20
    let "a = $1 + 30"
    echo $a # 30 + first command line argument
    
Some basic expresssions:

    +, -, /*, / 	addition, subtraction, multiply, divide
    var++ 	        Increase the variable var by 1
    var-- 	        Decrease the variable var by 1
    % 	        Modulus (Return the remainder after division)
    
``expr`` is similar to ``let`` except instead of saving the result to a variable it instead prints the answer. 
It also common to use expr within command substitution to save the output to a variable.    

    #!/bin/bash
    expr 5 + 4
    expr "5 + 4"
    expr 5+4
    expr 5 \* $1
    expr 11 % 2
    a=$( expr 10 - 3 )
    echo $a # 7
    
    user@bash: ./expr_example.sh 12
    9
    5 + 4
    5+4
    60
    1
    7

 **Double Parentheses**
 
    $(( expression ))
    
Double parentheses allows variable assignment with arithmetic. It is quite flexible in how you format it's expression.
For example, you do not need to escape certain characters. 

    #!/bin/bash
    a=$(( 4 + 5 ))
    echo $a # 9
    a=$((3+5))
    echo $a # 8
    b=$(( a + 3 ))
    echo $b # 11
    b=$(( $a + 4 ))
    echo $b # 12
    (( b++ ))
    echo $b # 13
    (( b += 3 ))
    echo $b # 16
    a=$(( 4 * 5 ))
    echo $a # 20

**Length of a variable**

    #!/bin/bash
    # Show the length of a variable.
    a='Hello World'
    echo ${#a} # 11
    b=4953
    echo ${#b} # 4

    