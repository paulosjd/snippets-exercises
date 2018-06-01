**Everything is a file**

A text file is a file, a directory is a file, your keyboard is a file (one that the system reads from only), your monitor is a file (one that the system writes to only) etc. Keeping this in mind  helps with understanding the behaviour of Linux as we manage files and directories.

**Linux is an Extensionless System**

Files can have any extension they like or none at all. A file extension is normally a set of 2 - 4 characters after a full stop at the end of a file, which denotes what type of file it is. In other systems such as Windows the extension is important and the system uses it to determine what type of file it is. Under Linux the system actually ignores the extension and looks inside the file to determine what type of file it is. So for instance I could have a file myself.png which is a picture of me. Sometimes be hard to know for certain what type of file a particular file is. Luckily there is a command called ``file`` which we can use to find this out.

    user@bash: file [path]

[path] is used here since  whenever we specify a file or directory on the command line it is actually a path. Also because directories just a special type of file, it would be more accurate to say that a path is a means to get to a particular location in the system and that location is a file.  Appreciate that whenever we refer to a file or directory on the command line it is in fact a path. As such it may be specified as either an absolute or relative path.

Linux is case sensitive. As such it is possible to have two files or directories with same name but different cases. Spaces are used to separate items on the command line so for spaces in names, must either use e.g. cd 'my folder', or cd my\ folder.

**Hidden Files and Directories**

If the file or directory's name begins with a full stop then it is considered to be hidden. Files and directories may be hidden for a variety of reasons, such as if aren't needed in everyday use. The ``ls`` command can be modified by including the option -a so that it does show hidden files and directories. e.g. ls -a Documents


**Permissions**

Linux permissions dictate 3 things you may do with a file, read, write and execute, indicated with a single letter:

    r read - you may view the contents of the file.
    w write - you may change the contents of the file.
    x execute - you may execute or run the file if it is a program or script.

For every file we define 3 sets of people for whom we may specify permissions:

    owner - a single person who owns the file. 
    group - every file belongs to a single group.
    others - everyone else who is not in the group or the owner.

To view permissions for a file we use the long listing option for the command ls. In the output, the first character identifies the file type. If it is a dash ( - ) then it is a normal file. If it is a d then it is a directory. The same series of permissions may be used for directories but they have a slightly different behaviour. The following 3 characters represent the permissions for the owner. A letter represents the presence of a permission and a dash ( - ) represents the absence of a permission. In the folowing example the owner has all three permissions. The following 3 characters represent the permissions for the group. In this example the group has the ability to read but not write or execute. Note that the order of permissions is always read, then write then execute. Finally the last 3 characters represent the permissions for others (or everyone else). In this example they have the execute permission and nothing else.

    user@bash: ls -l /home/ryan/linuxtutorialwork/frog.png  
    -rwxr----x 1 harry users 2.7K Jan 4 07:32 /home/ryan/linuxtutorialwork/frog.png
    
To change permissions on a file or directory we use a command called ``chmod`` which has permission arguments that are made up of 3 components:

    Who are we changing the permission for? [ugoa] - user (or owner), group, others, all
    Are we granting or revoking the permission - indicated with either a plus ( + ) or minus ( - )
    Which permission are we setting? - read ( r ), write ( w ) or execute ( x )

    chmod [permissions] [path]

 bash (The program that provides the command line interface) 

    user@bash: chmod g+x frog.png
    user@bash: ls -l frog.png
    -rwxr-x--x 1 harry users 2.7K Jan 4 07:32 frog.png

A program is a series of instructions that tell the computer what to do. When we run a program, those instructions are copied into memory and space is allocated for variables and other stuff required to manage its execution. This running instance of a program is called a process and it's processes which we manage.

Process Management
-----------------

**What is Currently Running**

As well as the processes we are running, there may be other users on the system also running stuff and the OS itself will usually also be running various processes which it uses to manage everything in general. To see what is currently happening on the system we may use a program called ``top``. Line 2 shows the running processes, most of these will be system processes. Line 3 and 4 shows working memory (RAM) and virtual memory on the system. Lines 6 - 10 is a listing of the most resource intensive processes on the system. The PID column identifies the Process ID.

    user@bash: top
    Tasks: 174 total, 3 running, 171 sleeping, 0 stopped
    KiB Mem: 4050604 total, 3114428 used, 936176 free
    Kib Swap: 2104476 total, 18132 used, 2086344 free
 
    PID USER %CPU %MEM COMMAND
    6978 ryan 3.0  21.2 firefox
    11 root 0.3   0.0 rcu_preemp
    6601 ryan 2.0   2.4 kwin

**Killing a Crashed Process**

Identify using the program ps identified using grep. Then use a program called ``kill``. This sends signal to process effectively asking the program nicely to quit, if it does not supply signal -9 which effectively means go in with a sledge hammer.

    user@bash: ps aux | grep 'firefox'
    ryan 6978 8.8 23.5 2344096 945452 ? Sl 08:03 49:53 /usr/lib64/firefox/firefox
    kill 6978
    kill -9 6978