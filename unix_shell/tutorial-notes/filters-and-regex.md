**More on the Running of Commands**

Command line options can modify the behaviour of our commands to suit our needs. A lot of these have both a long hand and short hand version, e.g. ``ls -a`` and ``ls --all``.  One advantage of using long hand is that it can be easier for you to remember what your commands are doing. One advantage of using shorthand is that you can chain multiple together easier e.g. ``ls -alh``. 
There are a few useful options available for ``mkdir. -p`` which tells mkdir to make parent directories as needed (demonstration of what that actually means below). The second one is -v which makes mkdir tell us what it is doing:

    user@bash: mkdir -p linuxtutorialwork/foo/bar
    user@bash: mkdir -pv linuxtutorialwork/foo/bar
    mkdir: created directory 'linuxtutorialwork/foo'

In it's default behaviour ``cp`` will only copy a file, unless using wildcards. Using the -r option, which stands for recursive, we may copy directories. Recursive means that we want to look at a directory and all files and directories within it, and for subdirectories, go into them and do the same thing and keep doing this. Similary, to remove a non-empty directory, use the rm command with the -r option.

Moving and renaming files are the same

    user@bash:  mv [options] <source> <destination>

**Wildcards**

Wildcards are a set of building blocks that allow you to create a pattern defining a set of files or directories. They provides a means to play about with a set of files at once. Whenever we refer to a path we may also use wildcards in that path to turn it into a set of files or directories. Here is the basic set of wildcards and some examples:

    * - represents zero or more characters
    ? - represents a single character
    [] - represents a range of characters

    user@bash: ls
    barry.txt blah bob example.png firstfile foo1.txt foo2
    user@bash: ls b*
    barry.txt blah bob
    user@bash: ls /home/linuxtutorial/*.txt
    /home/linuxtutorial/barry.txt /home/linuxtutorial/blah.txt
    user@bash: ls ?i*
    firstfile video.mpeg
    user@bash: ls [sv]*
    secondfile video.mpeg
    user@bash: mv my_images/*.??g backup/images/

**Filters**

``filter`` is a program that accepts textual data and then transforms it in a particular way. Filters are a way to take raw data, either produced by another program, or stored in a file, and manipulate it. Using Piping and Redirection (see following section) allows input via other means that add a lot more power.

    head [-number of lines to print] [path]
    tail [-number of lines to print] [path]
    sort [-options] [path]
    nl [-options] [path]
    cut [-options] [path]

``cut`` is useful if your content is separated into fields (columns) and you only want certain fields. Cut defaults to using the TAB character as a separator to identify fields. In a CSV file the separator is typically a comma ( , ) so can apply this accordingly with the -d option (delimiter). The -f option allows us to specify which field or fields we would like.

    user@bash: cut -f 1 -d ' ' mysampledata.txt 
    Fred
    Susy
    ...

    user@bash: cut -f 1 -d ' ' mysampledata.txt 
    Fred apples
    Susy oranges
    ...

    sed <expression> [path]

``sed`` stands for Stream Editor and it allows us to do a search and replace on our data, as in this basic example. A basic expression is of the following format: s/search/replace/g

    sed 's/oranges/bananas/g' mysampledata.txt
    Fred apples
    Susy bananas
    ...

**Grep and Regular Expressions**

Regular expressions are similar to the wildcards but they are a bit more powerful. They allow us to create a pattern and are typically used to identify and manipulate specific pieces of data. eg. identify every line containing an email address or a url in a set of data. The following examples demonstrate Re's with ``grep`` but many other programs use them (including sed and vi). ``egrep`` is a program which will search a given set of data and print every line which contains a given pattern. 

    egrep [command line options] <pattern> [path]

Let's say we wished to identify every line which contained the string mellon: 

    user@bash: egrep 'mellon' mysampledata.txt
    Mark watermellons 12
    Oliver rockmellons 2

    user@bash: egrep -n 'mellon' mysampledata.txt
    3:Mark watermellons 12
    8:Oliver rockmellons 2

    user@bash: egrep -c 'mellon' mysampledata.txt
    2

Regular expression basic building blocks: 
    
    . (dot) - a single character.
    ? - the preceding character matches 0 or 1 times only.
    * - the preceding character matches 0 or more times.
    + - the preceding character matches 1 or more times.
    {n} - the preceding character matches exactly n times.
    {n,m} - the preceding character matches at least n times and not more than m times.
    [agd] - the character is one of those included within the square brackets.
    [^agd] - the character is not one of those included within the square brackets.
    [c-f] - the dash within the square brackets operates as a range. In this case it means either the letters c, d, e or f.
    () - allows us to group several characters to behave as one.
    | (pipe symbol) - the logical OR operation.
    ^ - matches the beginning of the line.
    $ - matches the end of the line. 

    user@bash: egrep '[aeiou]{2,}' mysampledata.txt
    Robert pears 4
    Lisa peaches 7
    Anne mangoes 7
    Greg pineapples 3

In the following, in the first example the multiplier + applies to the . which is any character, the second the number 2 is the last character on the line, the third each line contains either 'is' or 'go' or 'or'. 

    user@bash: egrep '2.+' mysampledata.txt
    Fred apples 20

    user@bash: egrep '2$' mysampledata.txt
    Mark watermellons 12
    Susy oranges 12
    Oliver rockmellons 2

    user@bash: egrep 'or|is|go' mysampledata.txt
    Susy oranges 5
    Terry oranges 9
    Lisa peaches 7
    Susy oranges 12
    Anne mangoes 7

    user@bash: egrep '^[A-K]' mysampledata.txt
    Fred apples 20
    Anne mangoes 7
    Greg pineapples 3
    Betty limes 14