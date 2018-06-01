    $ read -p "Would you like some breakfast? [y/n] "
    Would you like some breakfast? [y/n] n
    $ if [[ $REPLY = y ]]; then
    >     echo "Here is some toast"   
    > else
    >     echo "Here, you should at least have a coffee"
    > fi
    Here, you should at least have a coffee
    
**The `if` Compound**

    if ! rm hello.txt; then echo "Couldn't delete hello.txt." >&2; exit 1; fi
    if rm hello.txt; then echo "Successfully deleted hello.txt."
    else echo "Couldn't delete hello.txt." >&2; exit 1; fi
    if mv hello.txt ~/.Trash/; then echo "Moved hello.txt into the trash."
    elif rm hello.txt; then echo "Deleted hello.txt."
    else echo "Couldn't remove hello.txt." >&2; exit 1; fi
    
We start with the `if` keyword, followed by a command list. This command list will be executed by bash, and upon completion, bash will hand the final exit code to the if compound to be evaluated. If the exit code is zero (0 = success), the first branch will be executed. Otherwise, the first branch will be skipped.
If one or more elif branches are available, these will in-turn execute and evaluate their own command list, and if successful execute their branch. Note that as soon as any branch of the if compound is executed, the remaining branches are automatically skipped: only one single branch is ever executed.

**Conditional test commands**

The `[[` keywords are simple, ordinary commands and are not some special form of if-syntax.
The `[[` command name takes a list of arguments and its final argument must be `]]`. The `&&` and `||` operators are 'and' and 'or' operators. 

    $ [[ Jack = Jane ]] && echo "Jack is Jane" || echo "Jack is not Jane"
    Jack is not Jane
    $ [[Jack = Jane ]] && echo "Jack is Jane" || echo "Jack is not Jane"
    -bash: [[Jack: command not found
    $ [[ Jack=Jane ]] && echo "Jack is Jane" || echo "Jack is not Jane"
    Jack is Jane
    
The first statement was written correctly and we got the expected output. The second is missing a space. The third behaves unexpected because the equality test requires spaces between the equals sign.
    
    
    
    
    
    
    
    