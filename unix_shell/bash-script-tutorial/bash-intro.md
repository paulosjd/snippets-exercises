All programs can read files, start other programs, do math, control devices etc.
The main difference between bash and most other programs is that bash was 
programmed to take commands from you, through the bash shell language.

In essence, a shell program is one that provides users with an interface to 
interact with other programs. Its simplicity makes it very easy for us as humans 
to find consistent structure in how we can interpret the text that appears in it and how we can issue our commands.
Bash is a simple tool in a vast toolbox of programs that lets me interact with my system using a text-based interface. 
It is a simple executable program located on a systems standard binary directories. A binary is an executable program that contains "binary code" which is executed directly by the system's kernel.

In interactive mode, the bash shell waits for your commands before performing them. Each command you pass it is executed.
Non-interactive mode: A bash script is a pre-written series of commands which are generally saved in files and subsequently used to automate a wide range of tasks.

There are a number of factors which can go into good, clean, quick, shell scripts.

The most important criteria must be a clear, readable layout. Since the main control structures are if/then/else and loops, indentation is critical for understanding what a script does.

Second is avoiding unnecessary commands. Consider the following:

    cat /tmp/myfile | grep "mystring"
    
The OS has to load up the /bin/grep executable, open a pipe in memory for the transfer, and run the /bin/cat executable. This would run much faster as:

    grep "mystring" /tmp/myfile 
    
**Commands and Arguments**

A bash command is the smallest unit of code that bash can independently execute. While executing a command, you cannot interact with the bash shell. As soon as bash is done executing a command, it returns to you for the next command to execute.
 
Most commands will only constitute one line and, unless the syntax of your bash command explicitly indicates that your command is not yet complete, as soon as you end that line, bash will immediately consider that to be the end of the command.

    $ if [[ $name = $USER ]]; then
    echo "Hello, me."
    
The first line of the if command in the example above doesn't contain enough information for bash to know what to do next.
As a result, bash shows a special prompt: >.  When we end that line, bash knows that you're done providing conditional result cases. It immediately begins running all the code in the entire block, from if to fi.

The above code could be run from a file instead:

    read -p "Your name? " name
    if [[ $name = $USER ]]; then
        echo "Hello, me."
    else
        echo "Hello, $name."
    fi
    
    $ bash hello.txt   
    Your name? James 
    Hello, James.
    Our new "bash" process ends when there is no code left in the file.

By making this a bash script (by adding #!/usr/bin/bash) we have a program that can be executed by the kernel. The 'shebang'
line tells the kernel what interpreter it needs to use to understand it.

Bash is a lax language interpreter, which means it will permit you to write ambiguous commands. Its syntax will not prevent you from writing commands that do things that are not what they seem. It is solely your responsibility to learn the syntax adequately, recognize the pitfalls and pick up the discipline to stick to the practices that avoid buggy code consistently.

**Basic Grammar**

     [ var=value ... ] name [ arg ... ] [ redirection ]
     
Before the command's name you can optionally put a few var assignments. These variable assignments apply to the environment of this one command only. 
The command's name is the first word (after the optional assignments). Bash finds the command with that name and starts it.
A command's name is optionally followed by a list of arg words, the command arguments. 
A command can also have a set of redirection operations applied to it. If you recall our explanation of file descriptors in an earlier section, redirections are the operations that change what the file descriptor plugs point to and change the streams that connect to our command processes. 

Many command types are syntax sugar: their effect can be achieved differently, but they exist to make the job easier.

Pipelines
 
Pipes are an example of 'syntax sugar', which make common tasks easier to perform than using basic syntax.
They are a convenient way of "connecting" two commands by way of linking the first process standard output to the second process' standard input.
Bash will create a subshell for each command and set up the first command's standard output file descriptor such that it points to the second command's standard input file descriptor. The two commands will run simultaneously and bash will wait for both of them to end.
Inbetween the two commands goes the | symbol. Alternatively, we can use the `|&` symbol in between the commands to indicate that we want not only the standard output of the first command, but also its standard error to be connected to the second command's input. This is usually undesirable since the standard error file descriptor is normally used to convey messages to the user. If we send those messages to the second command rather than the terminal display, we need to make sure the second command can handle receiving these messages.

Lists

A script is essentially a list of commands on separate lines, it is effectively a command list that uses newlines as the control operators between all the commands. is a command list: one command after another. Commands in lists are separated by a control operator.
The simplest control operator is just starting a new line, which is equivalent to ; and tells bash to just run the command and wait for it to end before advancing to the next command in the list. The second example uses the || control operator which tells bash to run the command before it as it normally would, but after finishing that command move to the next command only if the command before it failed.
If the command before it didn't fail, the || operator will make bash skip the command after it. This is useful for showing error messages when a command fails.

**Compound Commands**

These  behave as a single command in a command list. E.g. a block itself behaves as a single big command but inside it are a bunch of "sub" commands.

    $ if ! rm hello.txt; then echo "Couldn't delete hello.txt." >&2; exit 1; fi
    $ rm hello.txt || { echo "Couldn't delete hello.txt." >&2; exit 1; }
    
Both examples perform the same operation. The first example is a compound command, the second is a compound command in a command list.
The command on the right side of || operator is skipped unless the command before it fails.
The compound command in the second example begins at { and continues until the next }, as a result everything inside the braces is considered a single command, meaning we have a command list of two commands: the rm command followed by the { ... } compound. If we were to forget the braces, we would get a command list of three commands: the rm command followed by the echo command, followed by the exit command. The difference is mainly important to the || operator in deciding what to do when the rm command before it succeeds. If the rm succeeds, || will skip the command after it, which, if we leave out the braces, would be only the echo command. The braces combine the echo and exit commands into a single compound command, allowing || to skip both of them when rm succeeds.

**Functions**

You begin by specifying a name for your function. This is the name of your new command, you'll be able to run it later on by writing a simple command with that name.
After the command name go the () parentheses. Some languages use these parentheses to declare the arguments the function accepts: bash does not.
Next comes the compound command that will be executed each time you run the function.

**Command names and running programs**

     [ var=value ... ] name [ arg ... ] [ redirection ... ]
     
 The name tells bash what the job is that you want this command to perform. To figure out what you want your command to do, bash performs a search to find out what to execute. In order, bash uses the name to try and find either a function, a builtin, or a program (external command)

Functions are previously defined blocks of code given a name. Builtins are tiny procedures built into bash. They are small operations that were programmed into bash and bash doesn't need to run a special program to be able to perform them
our system has a great many programs installed. Some of them run in the terminal, some of them run invisibly, others run in your graphical interface. Bash finds programs by looking into your system's configured PATH
 
 **The PATH to a program**
 
Some programs will be installed in /bin, others in /usr/bin, yet others in /sbin and so on.
Your PATH variable contains a set of directories that should be searched for programs.

        PATH=/bin:/sbin:/usr/bin:/usr/sbin
           │     │
           │     ╰──▶ /sbin/ping ?  found!
           ╰──▶ /bin/ping ?  not found.
           
If you need to when the location of a program, you can use the ``type`` builtin:
           
    $ type ping
    ping is /sbin/ping
    $ type -a echo 
    echo is a shell builtin
    echo is /bin/echo

Sometimes you'll need to run a program that isn't installed in any of the PATH directories. In that case, you'll have to manually specify the path to where bash can find the program, rather than just its name.

    $ ./hello.txt
    Your name? 

 Bash only performs a PATH search on command names that do not contain a / character. Command names with a slash are always considered direct pathnames to the program to execute.
 
 You can add more directories to your PATH. A common practice is to have a /usr/local/bin and a ~/bin (where ~ represents your user's home directory). Remember that PATH is an environment variable: you can update it like this:
 
    $ PATH=~/bin:/usr/local/bin:/bin:/usr/bin
    
**Command arguments and quoting literals**

    [ var=value ... ] name [ arg ... ] [ redirection ... ]
    
Commands generally can't do much without more details, more context. Arguments are words separated by blank space. When we say words in the context of bash, we do not mean linguistic words. In bash, a word is defined as a sequence of characters considered as a single unit by the shell. A word is also known as a token.
To the bash shell, blank space is syntax just like anything else. It means: "break the previous apart from the next thing". Bash calls this: word splitting.
The importance of quoting cannot be overstated. The nice thing about quotes is that while it is sometimes unnecessary, it is rarely ever wrong to quote your data. 

You should use "double quotes" for any argument that contains expansions (such as $variable or $(command) expansions) and 'single quotes' for any other arguments. Single quotes make sure that everything in the quotes remains literal, while double quotes still allow some bash syntax such as expansions:

    echo "Good morning, $USER."
    echo 'Good morning' 
    
**Managing a command's input and output using redirection**

    [ var=value ... ] name [ arg ... ] [ redirection ... ]
    
Each process will generally have three standard file descriptors: standard input (FD 0), standard output (FD 1) and standard error (FD 2). When bash starts a program, it sets up a set of file descriptors for that program first. When you open your terminal to a new bash shell, the terminal will have set bash up by connecting bash's input and output to the terminal.
 
Each time bash starts a program of its own, it gives that program a set of file descriptors that match its own. This way, a bash command's messages end up on your terminal as well and your keyboard input ends up with the program (the command's output and input is connected to your terminal):

                 ╭──────────╮
    Keyboard ╾──╼┥0  bash  1┝╾─┬─╼ Display
                 │         2┝╾─┘
                 ╰──────────╯
If we want to gain control over where our commands connect to, we need to employ redirection.
        
    $ ls -l a b >myfiles.ls
    ls: b: No such file or directory

                 ╭──────────╮
    Keyboard ╾┬─╼┥0  bash  1┝╾─┬─╼ Display
              │  │         2┝╾─┤
              │  ╰─────┬────╯  │
              │        ╎       │
              │  ╭─────┴────╮  │
              └─╼┥0  ls    1┝╾─╌─╼ myfiles.ls
                 │         2┝╾─┘
                 ╰──────────╯

    $ cat myfiles.ls
    -rw-r--r--  1 lhunath  staff  0 30 Apr 14:43 a

Sometimes, though, we might find that error messages produced by some commands in our scripts are unimportant to the user and should be hidden. To do this:
    
    $ ls -l a b > myfiles.ls 2> /dev/null

 The file null is in the /dev directory: This is a special directory for device files. Device files are special files that represent devices in our system. When we write to or read from them, we're communicating directly with those devices through the kernel. The null device is a special device that is always empty. Anything you write to it will be lost and nothing can be read from it.
 
 What if we wanted to save all the output that would normally appear on the terminal to our myfiles.ls file; both the results and error messages?
 
    $ ls -l a b >myfiles.ls 2>&1
 
                  ╭──────────╮
    Keyboard ╾┬─╼┥0  bash  1┝╾─┬─╼ Display
              │  │         2┝╾─┘
              │  ╰─────┬────╯
              │        ╎
              │  ╭─────┴────╮
              └─╼┥0  ls    1┝╾─┬─╼ myfiles.ls
                 │         2┝╾─┘
                 ╰──────────╯   

 We use the `>&` operator, prefixing it with the file descriptor we want to change and following it with the file descriptor whose stream we need to "copy". You can translate the syntax 2>&1 as "Make FD 2 write(>) to where FD(&) 1 is currently writing."

Redirecting standard output and standard error:

    $ ping 127.0.0.1 &> results
    
This is a convenience operator which does the same thing as >file 2>&1 but is more concise. Again, you can append rather than truncate by doubling the arrow: &>>file

Here Documents and Here Strings:

Make FD 0 (standard input) read from the string between the delimiters, or read from the string.

    $ cat <<.
    > We choose . as the end delimiter.
    > Hello world.
    > Since I started learning bash, you suddenly seem so much bigger than you were before.
    > .

Here documents are a great way to feed large blocks of text to a command's input. They begin on the line after your delimiter and end when bash encounters a line with just your delimiter on it.
Here strings are very similar to here documents but more concise so generally preferred.

    $ cat <<<"Hello world.
    > Since I started learning bash, you suddenly seem so much bigger than you were before."

`exec`

In Bash the `exec` built-in replaces the shell with the specified program. It also allow us to manipulate the file descriptors. If you don't specify a program, the redirection after exec modifies the file descriptors of the current shell
if, for instance, you want to log the errors the commands in your script produce, just add at the beginning of your script:
 
    #!/usr/bin/env bash
    exec 2>myscript.errors
    .....
    
Let's see another use case. We want to read a file line by line, this is easy, we just do: 
    
    $ while read -r line;do echo "$line";done < file
    
Now, we want, after printing each line, to do a pause, waiting for the user to press a key. The might try the following but it would not work
as `read` would inherit the descriptor making it expecting input from file and not from our terminal:

    $ while read -r line;do echo "$line"; read -p "Press any key" -n 1;done < file
    
A quick look at help read tells us that we can specify a file descriptor from which read should read. Cool. Now let's use exec to get another descriptor, and it works:
 
    $ exec 3<file
    $ while read -u 3 line;do echo "$line"; read -p "Press any key" -n 1;done

Closing file descriptors

Closing a file through a file descriptor is easy, just make it a duplicate of -. For instance, let's close stdin <&- and stderr 2>&-: 
     
    exec 3>file
    .....
    #commands that uses 3
    .....
    exec 3>&-
    
    #we don't need 3 any more






