
**`jQuery.each( array, callback )`**

array: the array or array-like object to iterate over. For an array, the callback is passed an array index and a corresponding array value each time.

callback: the function that will be executed on every value.

    $.each([ 52, 97 ], function( index, value ) {
      alert( index + ": " + value );
    });

    // 0: 52
    // 1: 97

    // ajax jsonresponse python list to give appropriate options in select field
    $.each(data.mechanisms, function(key, value) {
        $("#mechanism_id")
            .append($('<option>', { value : key })
            .text(value.name));
    });

**`jQuery.each( object, callback )`**

If an object is used as the collection, the callback is passed a key-value pair each time:

    var obj = {
      "flammable": "inflammable",
      "duh": "no duh"
    };
    $.each( obj, function( key, value ) {
      alert( key + ": " + value );
    });

    // flammable: inflammable
    // duh: no duh

We can break the `$.each()` loop at a particular iteration by making the callback function return `false`.
The `$.each()` function is not the same as `$(selector).each()`, which is used to iterate, exclusively, over a jQuery object.



