Create a script in your home directory, add it to your PATH and then run the script as an ordinary command.

    #!/usr/bin/env bash
    echo "Hello world"
    
    $ PATH=$PATH:~/desktop/bash-scripts
    $ hello
    Hello world
    
Run a command that produces messages on both standard output and standard error. 
Send only the last command's standard error messages to a file called errors.log. Then show the contents of errors.log on the terminal.

    $ cat file myfile 2> errors.log
    Hello world
    $ cat errors.log
    cat: myfile: No such file or directory
    
Run a command containing a string, replace a word in the string using `sed` and save the output to a file

    $ sed 's/foo/bar/g' <<< 'var1 is foo' > myfile
    $ cat myfile
    var1 is bar

Write a script which takes a number between 2 and 9 as an arguments and prints it to the screen with a suffix e.g. 3rd for 3 

    #!/bin/bash
    if [ $1 = 2 ]
    then	
        echo "$1nd"
    fi
    if [ $1 -gt 2 ] && [ $1 -lt 10 ]
    then	
        echo "$1rd"
    fi
    if [ $1 -lt 2 ] || [ $1 -gt 10 ]
    then	
        echo "please enter number between 2 and 9"
    fi

Search for a certain process which is running and terminate it.

    $ ps aux | grep firefox
    # PID is 2196
    $ kill 2196
    
Assign the string hello to a variable, then assign to string ' world' to the end of its contents. Then show its last word.

    $ greet=hello
    $ greet+=' world'
    # remove anything before and including the first space
    $ echo ${greet#* }
    
Replace the first space character in the variable contents with ' big':

    $ greet="${greet/ / big}"
    
Redirect the contents of the variable into a file whose name is the value of the variable with the spaces replaced by underscores (_) and a .txt at the end:
   
   $ echo $greet > "${greet/ /_}.txt"
   
Start a new bash shell that outputs its first argument and pass Hello World! in as an argument to it.

    $ bash -c 'echo "$1"' -- 'Hello World'
    
Start a bash shell that outputs the third and fourth arguments passed in from 1, 2, The Third, Fourth:

    $ bash -c 'echo "${@:3}"' -- 1, 2, The Third, Fourth
    

    