When referring to or reading a variable we place a $ sign before the variable name.
When setting a variable we leave out the $ sign.
Some people like to always write variable names in uppercase so they stand out. It's your preference however.
 
**Command Line Arguments**
we use the variables $1 to represent the first command line argument, $2 to represent the second command line argument and so on. 
These are automatically set by the system when we run our script so all we need to do is refer to them:

    $0 - The name of the Bash script.
    $1 - $9 - The first 9 arguments to the Bash script. (As mentioned above.)
    $# - How many arguments were passed to the Bash script.
    $@ - All the arguments supplied to the Bash script.
    $? - The exit status of the most recently run process.
    $$ - The process ID of the current script.
    $USER - The username of the user running the script.
    $HOSTNAME - The hostname of the machine the script is running on.
    $SECONDS - The number of seconds since the script was started.
    $RANDOM - Returns a different random number each time is it referred to.
    $LINENO - Returns the current line number in the Bash script.

If you type the command env on the command line you will see a listing of other variables which you may also refer to.

**Setting Variables**

    #!/bin/bash
    # A simple variable example
    myvar=foo
    echo $myvar $1
    echo
    sampledir=/etc
    ls $sampledir
    
**Quotes**

hen we want variables to store more complex values however, we need to make use of quotes. This is because under normal
 circumstances Bash uses a space to determine separate items.
 
    user@bash: myvar='Hello World'
    user@bash: $myvar
    'Hello World'
    
**Command Substitution**

Command substitution allows us to take the output of a command or program 
and save it as the value of a variable. To do this we place it within brackets, preceded by a $ sign.

    user@bash: myvar=$( ls /etc | wc -l )
    user@bash: echo There are $myvar entries in the directory /etc

When playing about with command substitution it's a good idea to test your output rather than just assuming it will 
behave in a certain way.

**Exporting Variables**

Variables are limited to the process they were created in. If we want the variable to be available to the second script then 
we need to export the variable.

    #!/bin/bash
    # demonstrate variable scope 1.
    var1=blah
    var2=foo
    echo $0 :: var1 : $var1, var2 : $var2
    export var1
    ./script2.sh

    #!/bin/bash
    # demonstrate variable scope 2
    echo $0 :: var1 : $var1, var2 : $var2
    # Let's change their values
    var1=flop
    var2=bleh

    user@bash: ./script1.sh
    script1.sh :: var1 : blah, var2 : foo
    script2.sh :: var1 : blah, var2 :
    script1.sh :: var1 : blah, var2 : foo
    
In this example, ``export var1`` makes var1 available to the child process. Note that exporting variables is a one-way process.

Variables and Expansions
--------

    $ rm 'myfile1' myfile2'
    $ rm *
    
The above commands could be used to do the same thing but the first way is very limiting as it requires the arguments to be 
explicity passed. Even for the second requires manually going to the directory, finding out which files were present and issue an rm command.
To make a generic template to enable re-use, we need to remove all the specific context.

Pathname expansion can achieve this. In the above examples, bash notices the pathname pattern in the arguments. It then look on the file
system for pathname patterns which match. To perform pathname expansions we use the *glob pattern*:

    *                matches any kind of text, even no text at all.
    ?                matches any one single character.
    [characters]     set of characters within rectangular braces matches a single character, only if it's
                     in the given set.
    [[:classname:]]  Supported character classes include: alnum, alpha, ascii, blank, cntrl, digit, graph, lower, print,
                     punct, space, upper, word, xdigit
    
    $ ls 0?' '*.rtf
    09 Information docs.rtf
    $ ls [[:digit:]][[:digit:]]*
    02 myfile.py
    09 Information docs.rtf
    
Globs will never jump into subdirectories. They only match against file names in their own directory. If we want a glob to go looking at the pathnames in a different directory, we need to explicitly tell it with a literal pathname:
 
    ls ~/Downloads/*.txt
    ls ~/*/hello.txt

**Value Substitution and Command Substitution**

    $ echo "The file <hello.txt> contains: $(cat hello.txt)"
    
Bash will first run cat hello.txt, take the output of this command (which is our string Hello world.) and then expand our Command Substitution syntax (the $(cat ...) part) into that output.
    
Value expansions ($...) must always be double-quoted.

**Bash Parameters**

Bash parameters are regions in memory where you can temporarily store some information for later use.
Not unlike files, we write to these parameters and read from them when we need to retrieve the information later. But since we're using the system's memory and not the disk to write this information to, access is much faster. Using parameters is also much easier and the syntax more powerful than redirecting input and output to and from files.
Shell variables are the most common type.

**Shell Variables and Parameter Expansion**

Command substitution can be used in variable assignments:

    $ contents="$(cat hello.txt)"
    
Parameter expansions take the data out of the parameter and inlines it inlines it with the command. Double quotes should always be used. Wrapping the expansion with curly braces to specify the beginning and end of the parameter can be useful in cases:
 
    $ name=Britta time=23.73
    $ echo "$name's current record is $times."
    Britta's current record is .
    $ echo "$name's current record is ${time}s."
    Britta's current record is 23.73s.

Parameter expansions also allows parameter expansion operators to be used. Here, glob patterns are used (the `%` operator is used to removed the .seconds while the `#` operator removes the first part of the time value):

    $ echo "$name's current record is ${time%.*} seconds and ${time#*.} hundredths."
    Britta's current record is 23 seconds and 73 hundredths.
    
${parameter#pattern} Remove the *shortest* string that matches the pattern if it's at the *start* of the value:

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url#*/}"
    /guide.bash.academy/variables.html

${parameter##pattern} Remove the *longest* string that matches the pattern if it's at the *start* of the value:

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url##*/}"
    variables.html
    
${parameter%pattern} Remove the *shortest* string that matches the pattern if it's at the *end* of the value:

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url%/*}"
    http://guide.bash.academy
    
${parameter%%pattern} Remove the *longest* string that matches the pattern if it's at the *end* of the value:

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url%/*}"
    http:
    
${parameter/pattern/replacement} Replace the *first* string that matches the pattern with the replacement
    
    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url/./-}"
    http://guide-bash.academy/variables.html

${parameter//pattern/replacement} Replace *each* string that matches the pattern with the replacement

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url//./-}"
    http://guide-bash-academy/variables-html
    
${#parameter} Expand the length of the value (in bytes).

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${#url}"
    40
        
${parameter:start\[:length]} Expand a part of the value, starting at start, length bytes long

    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url:7}"
    guide.bash.academy/variables.html

${parameter\[^|^^|,|,,]\[pattern]}  Expand transformed as either upper- or lower-case all characters, or those matching the pattern). 
    
    $ url='http://guide.bash.academy/variables.html'   
    $ echo "${url^^[ht]}"
    HTTp://guide.basH.academy/variables.HTml   
    
**Environment Variables**

When you run a new program from the shell, bash will run this program in a new process. When it does, this new process will have its own environment. But unlike shell processes, ordinary processes do not have shell variables. They only have environment variables. More importantly, when a new process is created, its environment is populated by making a copy of the environment of the creating process:

    ╭─── bash ───────────────────────╮
    │             ╭────────────────╮ │
    │ ENVIRONMENT │ SHELL          │ │
    │             │ greeting=hello │ │
    │             ╰────────────────╯ │
    │ HOME=/home/lhunath             │
    │ PATH=/bin:/usr/bin             │
    ╰─┬──────────────────────────────╯
      ╎  ╭─── ls ─────────────────────────╮
      └╌╌┥                                │
         │ ENVIRONMENT                    │
         │                                │
         │ HOME=/home/lhunath             │
         │ PATH=/bin:/usr/bin             │
         ╰────────────────────────────────╯
         
Since the environment is specific to each process, changing or creating new variables in the child will in no way affect the parent
 While most of your variables will be ordinary shell variables, you may opt to "export" some of your shell variables into the shell's process environment. In doing so, you're effectively exporting your variable's data to each child process you create, and those child processes will in turn export their environment variables to their children. Your system uses environment variables for all sorts of things, mainly to provide state information and default configurations for certain processes.
 
 You can export your own variables into the environment. This is often done to configure the behavior of any programs you run. For instance, you can export LANG and assign it a value that tells programs what language and character set they should use. Environment variables are generally only useful to those programs that know about and support them explicitly. rm uses just LANG if present to determine the language for its error messages:
 
     ╭─── bash ───────────────────────╮
    │             ╭────────────────╮ │
    │ ENVIRONMENT │ SHELL          │ │
    │             │ greeting=hello │ │
    │             ╰────────────────╯ │
    │ HOME=/home/lhunath             │
    │ PATH=/bin:/usr/bin             │
    │ LANG=en_CA                     │
    │ PAGER=less                     │
    │ LESS=-i -R                     │
    ╰─┬──────────────────────────────╯
      ╎  ╭─── rm ─────────────────────────╮
      ├╌╌┥                                │
      ╎  │ ENVIRONMENT                    │
      ╎  │                                │
      ╎  │ HOME=/home/lhunath             │
      ╎  │ PATH=/bin:/usr/bin             │
      ╎  │ LANG=en_CA                     │
      ╎  │ PAGER=less                     │
      ╎  │ LESS=-i -R                     │
      ╎  ╰────────────────────────────────╯
      
**Positional Parameters**
      
These expand to values that were sent into the process as arguments when it was created by the parent. For instance, when you start a grep process using this command:

    $ grep Name registrations.txt

The grep command is run with two arguments. If grep were a bash script, the first and second arguments would be available in the script by expanding $1 and $2.
As with variable parameters, expansion operators can be used:
    
    #!/usr/bin/env bash
    echo "The Name Script"
    echo "usage: names 'My Full Name'"; echo
    
    first=${1%% *} last=${1##* } middle=${1#$first} middle=${middle%$last}
    echo "Your first name is: $first"
    echo "Your last name is: $last"
    echo "Your middle names are: $middle"

The script can be saved and run according to the usage description:

    $ chmod +x names
    $ ./names 'Maarten Billemont'
    The Name Script
    usage: names 'My Full Name'
    
    Your first name is: Maarten
    Your last name is: Billemont
    Your middle names are: 
 
When starting a new bash shell using the bash command, there is a way to pass in positional parameters. This allows passing a list of arguments to an inline bash script.
Passing the -c option followed by an argument that contains some bash shell code will tell bash that instead of starting a new interactive bash shell, you want to just have the shell run the provided bash code and finish.

    $ bash -vc 'echo "1: $1, 2: $2, 4: $4"' -- \
    > 'New First Argument' Second Third 'Fourth Argument'
    echo "1: $1, 2: $2, 4: $4"
    1: New First Argument, 2: Second, 4: Fourth Argument

Here we pass the -v argument to bash to show us the code it is going to run before the result. We can use \ at the end of a line to resume on a new line.
The first (zero-eth) argument is --. Whenever we put code in a string (such as in the case of passing it in as an argument), the code should be single-quoted. This is important because single quotes are much more reliable at making the wrapped data literal than double quotes.

**Special Parameters**

    "$@" 	rm "$@" 	
    Expands the positional parameters as a list of separate arguments.
    "$#" 	echo "Count: $#" 	
    Expands into a number indicating the amount of positional parameters that are available. 

**Shell Internal Variables**

The bash shell creates a number of variables which can be used for various tasks and for 
looking up certain state information from the shell or changing certain shell behaviours.

Internal shell variables are shell variables with uppercase names, as are environment variables. Be sure not to use the names of these when creating your own shell variables.
So as a rule you should make shell variables with lowercase names and environment variables with uppercase names.

    BASH 	/usr/local/bin/bash
    This variable contains the full pathname of the command that started the bash you are currently in.
    
    BASH_SOURCE 	myscript
    The scripts that are currently running, usually it is either empty or contains just the pathname of your script.
    
    BASHPID 	5345
    This contains the process ID of the bash that is parsing the script code.
    
    HOME 	/Users/lhunath
    Contains the pathname of the home directory of the user running the bash shell.
    
    HOSTNAME 	myst.local
    The name of your computer.
    
    LANG 	en_CA.UTF-8
    Used to indicate your preferred language category.
    
    MACHTYPE 	x86_64-apple-darwin16.0.0
    A full description of the type of system you are running.
    
    PWD 	/Users/lhunath
    The full pathname of the directory you are currently in.

**Arrays**

What if we wanted to create a variable that contains a list of all the files we want to delete? The answer is arrays:

    $ files=( myscript hello.txt "05 my photo.jpg" )
    $ rm "${files[@]}"
    
Syntactical spacing is used to separate distinct elements of the list.
Just like regular variable assignment, when space needs to be part of the variable's data, it must be quoted so that bash interpretes the space as literal. 
As always, it is essential to wrap parameter expansions in double quotes.
The expansion of the files parameter using the "${files[@]}" syntax effectively results in this:

    $ rm -myscript hello.txt "05 my photo.jpg"

Bash provides some other operations that we can perform on arrays:

    $files+=( selfie.png )
    Using the +=( ) operator we can append a list of items to the end of an array.   
    
    $ files=( *.txt )
    Just like in a command's arguments, we can expand glob patterns here.
    
    $ echo "${files[0]}"
    To expand a single item from an array, specify that item's ordinal number.
    
    $ echo "$files"
    If we forget the array expansion syntax, bash will expand only the first item.
    
    $ unset "files[3]"
    To remove a specific item from the array, we use unset.

Examples: 

    $ names=( "Susan Quinn" "Anne-Marie Davis" "Mary Tate" )
    $ echo "${names[@]/ /_}"
    Susan_Quinn Anne-Marie_Davis Mary_Tate
    
    $ echo "${#names[@]}"
    3
    $ echo "${#names[1]}"
    16

    $ echo "${names[@]:1:2}"
    Anne-Marie Davis Mary Tate
    $ echo "${names[@]: -2}"
    Anne-Marie Davis Mary Tate
    
In the last `echo` command, if we omit the space, the ${parameter:-value} operator is invoked, which substitutes a default value whenever parameter's value is empty.
