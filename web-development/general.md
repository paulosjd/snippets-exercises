One good example of usage of hooks, coincidentally in web development, are WordPress' hooks.

They are named appropriately in that they allow a way to 'hook into' certain points of the execution of a program.

So for example, the wp_head is an 'action' that is emitted when a WordPress theme is being rendered and it's at the part where it renders the part that's within the <head> tags. Say that you want to write a plugin that requires an additional stylesheet, script, or something that would normally go within those tags. You can 'hook into' this action by defining a function to be called when this action is emitted. Something like:

    add_action('wp_head', 'your_function');
    
    your_function() could be something as simple as:
    
    function your_function() {
        echo '<link rel="stylesheet" type="text/css" href="lol.css" />';
    }

Now, when WordPress emits this action by doing something like do_action('wp_head');, it will see that your_function() was 'hooked into' that action, so it will call that function (and pass it any arguments if it takes any, as defined in the documentation for any particular hook).

Long story short: It allows you to add additional functionality at specific points of the execution of a program by 'hooking into' those points, in most cases by assigning a function callback.