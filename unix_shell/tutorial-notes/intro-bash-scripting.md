A Bash script allows us to define a series of actions which the computer will then perform without us having to enter the commands ourselves. A script is interpreted (read and acted upon) by something called an interpreter. There are various interpreters on a typical linux system.

Anything you can run on the command line you may place into a script and they will behave exactly the same, and vice versa.
When testing different parts of your script, as you're building it, it is often easiest to just run your commands directly on the command line.

    user@bash: which bash
    /bin/bash

    user@bash: cat myscript.sh
    #!/bin/bash
    # A simple demonstration script
 
    echo Here are the files in your current directory:
    ls
    
    user@bash: ./myscript.sh
    Here are the files in your current directory:
    barry.txt bob example.png firstfile foo1 myoutput video.mpeg

The very first line of a script should always have the first two characters and then the path to the interpreter. Anything after # is a comment, e.g. include name, date, quick description.

**Why the ./ ?**

    user@bash: echo $PATH
    /usr/local/bin:/usr/bin:/bin:/usr/bin/X11:/usr/X11R6/bin:/usr/games:/usr/lib/mit/bin:/usr/lib/mit/sbin

When we type a command on the command line, the system runs through a preset series of directories, looking for the program we specified. We may find out these directories by looking at a particular variable PATH.

The system will look in the first directory and if it finds the program it will run it, if not it will check the second directory and so on. Directories are separated by a colon ( : ).

The system will not look in any directories apart from these, it won't even look in your current directory. We can override this behaviour however by supplying a path. 

Variables
---------

    user@bash: cat myvar.sh
    #!/bin/bash
    # A simple demonstration script
 
    name='Ryan'
    echo Hello $name
    
    user@bash: ./myvar.sh
    Hello Ryan

When we run a script, there are several variables that get set automatically for us. Here are some of them:

    $0 - The name of the script.
    $1 - $9 - Any command line arguments given to the script. $1 is the first argument, $2 the second and so on.
    $# - How many command line arguments were given to the script.
    $* - All of the command line arguments.

**Backticks**

I will make brief mention of the deprecated `...` syntax. Old-style bourne shells used this syntax for Command Substitution instead of the more modern $(...) syntax.

    user@bash: cat backticks.sh
    #!/bin/bash
    # A simple demonstration of using backticks
 
    lines=`cat $1 | wc -l`
    echo The number of lines in the file $1 is $lines

    user@bash: ./backticks.sh testfile.txt
    The number of lines in the file testfile.txt is 12

**A Sample Backup Script**

    user@bash: cat projectbackup.sh
    #!/bin/bash
    # Backs up a single project directory
 
    date=`date +%F`
    mkdir ~/projectbackups/$1_$date
    cp -R ~/projects/$1 ~/projectbackups/$1_$date
    echo Backup of $1 completed

    user@bash: ./projectbackup.sh ocelot
    Backup of ocelot completed

**If Statements**

    #!/bin/bash
    # Backs up a single project directory
    # Paul 17/3/2018
     
    if [ $# != 1 ]
    then
        echo Usage: A single argument which is the directory to backup
        exit
    fi
    if [ ! -d ~/projects/$1 ]
    then
        echo 'The given directory does not seem to exist (possible typo?)'
        exit
    fi
    date=`date +%F`
     
    # Do we already have a backup folder for todays date?
    if [ -d ~/projectbackups/$1_$date ]
    then
        echo 'This project has already been backed up today, overwrite?'
        read answer
        if [ $answer != 'y' ]
        then
            exit
        fi
    else
        mkdir ~/projectbackups/$1_$date
    fi
    cp -R ~/projects/$1 ~/projectbackups/$1_$date
    echo Backup of $1 completed

In the first if statement we are asking if the number of arguments ( $# ) is not equal to ( != ) one.  To indicate the end of an if statement we have a single line which has fi (if backwards) on it. 

In the second if statement, the exclamation mark ( ! ) means not, the -d means 'the path exists and is a directory'. So the line reads as 'If the given directory does not exist'. It is possible to ask the user for input. The command we use for that is read. read takes a single argument which is the variable to store the answer in.