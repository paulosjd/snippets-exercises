
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
