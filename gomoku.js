

$(document).ready(function(){
    for (i = 0; i <15; i++) { 
        for (j = 0; j <15; j++){
            $("#board").append("<div data-x='"+i+"' data-y='"+j+"' data-stone='"+"."+"' class=square>("+i+","+j+")<div>")    
        }
    }    

    $(".square").click(function(){
        // Holds the product ID of the clicked element
        var x = $(this).attr('data-x');
        var y = $(this).attr('data-y');
        var stone = $(this).attr('data-stone');
        clickSquare(x,y,stone);
    });
});


function clickSquare(x,y,stone){
    alert(x+" "+y+" "+stone);
}