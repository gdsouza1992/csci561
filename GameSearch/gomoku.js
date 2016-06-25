
var freeSpaces = []
var placedStones = []
var playerBlack = true;

$(document).ready(function(){

    //Setup the board with 15 X 15 tiles
    for (i = 0; i <15; i++) { 
        for (j = 0; j <15; j++){
            //Add data attribs for x and y cordinates and set the data stone to free space '.'
            $("#board").append("<div data-x='"+i+"' data-y='"+j+"' data-stone='"+"."+"' class=square><div class='stone'></div></div>")    
        }
    } 

    //Place the starting black stone at the center of the board
    //Remove the existing free space '.' and replace with 'b' from the parent <div>.
    var centerStone = $("#board div[data-x='7'][data-y='7'] .stone").addClass("black").parent().attr('data-stone','b');

    //Toggle the current player
    playerBlack = false

    //Get the 8 free spaces around center tile
    getConnected8(7,7);

    $(".square").click(function(){
        // Holds the product ID of the clicked element
        
        if($(this).hasClass("free")){
            $(this).unbind("click");
            var x = $(this).attr('data-x');
            var y = $(this).attr('data-y');
            var stone = $(this).attr('data-stone');
            $(this).removeClass("free");
            clickSquare(x,y,stone);
        }
    });
});


function clickSquare(x,y,stone){

    $("#temp").text("clicked "+x+","+y);
    if(playerBlack){
        //Assign a black stone at x,y
        $("#board div[data-x='"+x+"'][data-y='"+y+"'] .stone").addClass("black").parent().attr('data-stone','b');
        $.each(freeSpaces, function( index, value ) {
        if(value.X == x && value.Y == y)
            freeSpaces[index].value = 'b'
        });
    }else{
        //Assign a white stone at x,y
        $("#board div[data-x='"+x+"'][data-y='"+y+"'] .stone").addClass("white").parent().attr('data-stone','w');
        $.each(freeSpaces, function( index, value ) {
        if(value.X == x && value.Y == y)
            freeSpaces[index].value = 'w'
        });
    }
    //Toggle the current player
    playerBlack = !playerBlack;


    getConnected8(x,y);
}

function getConnected8(x,y){
    //Ensure concatenation doesnt occur and arithematic does.
    x=parseInt(x)
    y=parseInt(y)

    //Find the tile value in all 8 directions
    var north = GetStoneAt(x,y-1);
    var south = GetStoneAt(x,y+1);
    var east = GetStoneAt(x+1,y);
    var west = GetStoneAt(x-1,y);
    var northeast = GetStoneAt(x+1,y-1);
    var northwest = GetStoneAt(x-1,y-1);
    var southeast = GetStoneAt(x+1,y+1);
    var southwest = GetStoneAt(x-1,y+1);

    //Push the values to the global freeSpaces array if '.'
    if(north == '.')
        freeSpaces.push({"X":(x),"Y":(y-1),"value":north});
    if(south == '.')
        freeSpaces.push({"X":(x),"Y":(y+1),"value":south});
    if(east == '.')
        freeSpaces.push({"X":(x+1),"Y":(y),"value":east});
    if(west == '.')
        freeSpaces.push({"X":(x-1),"Y":(y),"value":west});
    if(northeast == '.')
        freeSpaces.push({"X":(x+1),"Y":(y-1),"value":northeast});
    if(northwest == '.')
        freeSpaces.push({"X":(x-1),"Y":(y-1),"value":northwest});
    if(southeast == '.')
        freeSpaces.push({"X":(x+1),"Y":(y+1),"value":southeast});
    if(southwest == '.')
        freeSpaces.push({"X":(x-1),"Y":(y+1),"value":southwest});
    
    allowFreeClicks();
    $("#board div[data-x='"+x+"'][data-y='"+y+"'].square").removeClass("free")
}

function allowFreeClicks(){
    $.each(freeSpaces, function( index, value ) {
        if(value.value == '.')
            $("#board div[data-x='"+value.X+"'][data-y='"+value.Y+"'].square").removeClass("free").addClass("free"); 
    });
}

function GetStoneAt(x,y){
    if($("#board>div[data-x='"+(x)+"'][data-y='"+(y)+"']>div").hasClass("black"))
        return 'b';
    else if($("#board>div[data-x='"+(x)+"'][data-y='"+(y)+"']>div").hasClass("white"))
        return 'w';
    else return '.';
}


// for(i=0;i<=freeSpaces.length;i++){
//     for(j=0;j<=freeSpaces.length;j++){
//         if(i != j)
//             if(freeSpaces[i].X == freeSpaces[j].X && freeSpaces[i].Y == freeSpaces[j].Y)
//                 return i;
//     }
// }
    

// function getObjects(obj, key, val) {
//     var objects = [];
//     for (var i in obj) {
//         obj[i].X
//         obj[i].Y
//     }
//     return objects;
// }
