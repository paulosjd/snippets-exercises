Indenting is not required but is conventially used to improve readability and avoid simple mistakes. 
   
    #!/bin/bash
    if [ $1 -gt 100 ]
    then
        echo Hey that\'s a large number.
        pwd
    fi
    date

The square brackets in the if statement above are actually a reference to the command ``test``. This means that all of the operators that test allows may be used here as well.
 
    ! EXPRESSION 	        The EXPRESSION is false.
    -n STRING 	        The length of STRING is greater than zero.
    -z STRING               The lengh of STRING is zero (ie it is empty).
    STRING1 = STRING2    	STRING1 is equal to STRING2
    STRING1 != STRING2   	STRING1 is not equal to STRING2
    INTEGER1 -eq INTEGER2 	INTEGER1 is numerically equal to INTEGER2
    INTEGER1 -gt INTEGER2 	INTEGER1 is numerically greater than INTEGER2
    INTEGER1 -lt INTEGER2 	INTEGER1 is numerically less than INTEGER2
    -d FILE 	        FILE exists and is a directory.
    -e FILE 	        FILE exists.
    -r FILE 	        FILE exists and the read permission is granted.
    -s FILE 	        FILE exists and it's size is greater than zero (ie. it is not empty).
    -w FILE 	        FILE exists and the write permission is granted.
    -x FILE 	        FILE exists and the execute permission is granted.
    
When we refer to FILE above we are actually meaning a path. Remember that a path may be absolute or relative and may refer to a file or a directory.
Because [ ] is just a reference to the command test we may experiment and trouble shoot with test on the command line to make sure our understanding of its behaviour is correct.


    #!/bin/bash
    # Nested if statements
    if [ $1 -gt 100 ]
    then
        echo Hey that\'s a large number.
        if (( $1 % 2 == 0 ))
        then
            echo And is also an even number.
    fi
    fi

**If Else and If Elif Else**

    #!/bin/bash
    # else example
    if [ $# -eq 1 ]
    then
        nl $1
    else
        nl /dev/stdin
    fi


    #!/bin/bash
    # elif statements
    if [ $1 -ge 18 ]
    then
        echo You may go to the party.
    elif [ $2 == 'yes' ]
    then
        echo You may go to the party but be back before midnight.
    else
        echo You may not go to the party.
    fi

**Boolean Operations**

    and - &&
    or - ||

    #!/bin/bash
    # and example
    if [ -r $1 ] && [ -s $1 ]
    then
        echo This file is useful.
    fi


    if [ $USER == 'bob' ] || [ $USER == 'andy' ]
    then
        ls -alh
    else
        ls
    fi
    
**Case Statements**

    case <variable> in
    <pattern 1>)
      <commands>
      ;;
    <pattern 2>)
      <other commands>
      ;;
    esac

Use where we may take different paths depending on a variable matching a series of patterns. In such cases we could use if and elif statements but 
using the case statement makes things cleaner:


    #!/bin/bash
    case $1 in
      start)
        echo starting
        ;;
      stop)
        echo stoping
        ;;
      restart)
        echo restarting
        ;;
    *)
        echo don\'t know
        ;;
    esac
    
    user@bash: ./case.sh start
    starting
    user@bash: ./case.sh restart
    restarting
    user@bash: ./case.sh blah
    don't know