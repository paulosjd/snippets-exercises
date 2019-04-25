A context manager in Python is simply a protocol which:


0) `__getattribute__` on class
1) data descriptor on class
2) __dict__
3) non-data descriptor on class
4) simple value from the class
5) __getattr__ on class
6) raise AttributeError



    1) Add full name property to each object in array
    2) Return array of full names

    var oldArr = [{first_name:"Colin",last_name:"Toh"},{first_name:"Addy",last_name:"Osmani"},{first_name:"Yehuda",last_name:"Katz"}];
    function getNewArr(){
        return oldArr.map(function(item,index){
            item.full_name = [item.first_name,item.last_name].join(" ");
            return item;
        });
    }



        var p = [1,2,3,4]
    p.map(n => n *2)
    // Array [ 2, 4, 6, 8 ]
