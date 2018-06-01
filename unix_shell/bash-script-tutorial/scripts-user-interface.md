**Supplying data**

Remember there are 3 ways in which you may supply data to a Bash script:

    As command line arguments
    Redirected in as STDIN
    Read interactively during script execution

Your script may use one or a combination of these but should always aim to be the most convenient for the user.

Command line arguments are good as they will be retained in the users history making it easy for them to rerun commands. Command line arguments are also convenient when the script is not run directly by the user (eg, as part of another script or a cron task etc).

Redirected from STDIN is good when your script is behaving like a filter and just modifying or reformatting data that is fed to it.

Reading interactively is good when you don't know what data may be required until the script is already running

**Input Flexibility**

Think about how strict you are going to be with supplied data as well. The more flexible you can be the happier the end user is going to be. Think of someone supplying a date as an argument. They could supply the date as:
15-04-2018, 15/04/2018, or 15:04:2018.

We could write our script to insist on input in only one particular format. This would be easiest for us but potentially not convenient for the end user. What if they want to feed the date in as provided from another command or source that provides it in a different format?

We should always aim to be most convenient for the end user as oposed to ourselves. After all, we'll write it once but they will run it many times.

The command sed can easily allow us to accommodate many formats for input data.

    #!/bin/bash
    # A date is the first command line argument
    clean_date=$( echo $1 | sed 's/[ /:\^#]/-/g' )
    echo $clean_date

**Making code readable**

Take the time to structure your code well and later on you'll be thankful you did.

    Indent your code and space it out well so that different sections are easily distinguished.
    Name variables and functions with descriptive names so it is clear what they represent and do.
    Use comments where appropriate to explain a bit of code who's operation is not immediately obvious.

