**Vi Text Editor**

Vi is a command line text editor. There are two modes in Vi. Insert (or Input) mode and Edit mode. When you run this command it opens up the file. If the file does not exist then it will create it for you then open it up.

    user@bash: vi firstfile
    ~
    ~
    ~
    ~
    ~
    "firstfile" [New File]

You always start off in edit mode so the first thing we are going to do is switch to insert mode by pressing i. You can tell when you are in insert mode as the bottom left corner will tell you. After typing text press Esc which will take you back to edit mode. Saving and editing:
    
    ZZ (Note: capitals) - Save and exit
    :q! - discard all changes, since the last save, and exit
    :w - save file but don't exit
    :wq - again, save and exit
