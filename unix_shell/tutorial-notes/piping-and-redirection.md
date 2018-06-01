Every program we run on the command line automatically has three data streams connected to it.

    STDIN (0) - Standard input (data fed into the program)
    STDOUT (1) - Standard output (data printed by the program, defaults to the terminal)
    STDERR (2) - Standard error (for error messages, also defaults to the terminal)

**Redirecting to a File**

The greater than operator indicates to the command line that we wish the programs output to be saved in a file instead of printed to the screen. If we redirect to a file which does not exist, it will be created automatically for us. If we save into a file which already exists, however, then it's contents will be cleared, then the new output saved to it. We can instead get the new data to be appended to the file by using the double greater than operator.

    user@bash: wc -l my_list.txt > myoutput
    user@bash: cat myoutput
    7 my_list.txt
    user@bash: wc -l todo.txt >> myoutput

**Redirecting from a File**

If we use the less than operator we can read data from the file and feed it into the program via it's STDIN stream.

    user@bash: wc -l < myoutput
    8

**Redirecting Standard Error**

    user@bash: ls -l video2.mpg 2> errors.txt
    -rwxr--r-- 1 ryan users 6 May 16 09:14 video.mpg
    user@bash: cat errors.txt
    ls: cannot access blah.foo: No such file or directory

to save both normal output and error messages into a single file.

    user@bash: ls -l video.mpg blah.foo > myoutput 2>&1

**Piping**

Piping is a mechanism for sending data from one program to another. 
    
    user@bash: ls
    barry.txt bob example.png firstfile foo1 myoutput video.mpeg
    user@bash: ls | head -3
    foo.txt
    bar
    example.png
    user@bash: ls | head -3 | tail -1
    example.png

When writing pipes, it is often best if you build your pipes up incrementally. Run the first program and make sure it provides the output you were expecting. Then add the second program and check again before adding the third and so on. 

Combining pipes and redirection: 
    user@bash: ls | head -3 | tail -1 > myoutput

Feed the output of a program into the program less so that we can view it easier:

    user@bash: ls -l /etc | less
    (Full screen of output)

Identify all files in your home directory which the group has write permission for:

    user@bash: ls -l ~ | grep '^.....w'
    drwxrwxr-x 3 ryan users 4096 Jan 21 04:12 dropbox