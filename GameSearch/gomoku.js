
var freeSpaces = []
var placedStones = []
var playerBlack = true;
var AIturn = false;
var gameover = false;
var gameboard = "...............,...............,...............,...............,...............,...............,...............,...............,...............,...............,...............,...............,...............,...............,...............";
String.prototype.replaceAt=function(index, character) {
    return this.substr(0, index) + character + this.substr(index+character.length);
}

$(document).ready(function(){

    //Setup the board with 15 X 15 tiles
    for (i = 0; i <15; i++) {
        for (j = 0; j <15; j++){
            //Add data attribs for x and y cordinates and set the data stone to free space '.'
            $("#board").append("<div data-x='"+i+"' data-y='"+j+"' data-stone='"+"."+"' class=square><div class='stone'></div></div>")
        }
    }

    var squareWidth = $('.square').width();
    $('.square').height(squareWidth)

    //Place the starting black stone at the center of the board
    //Remove the existing free space '.' and replace with 'b' from the parent <div>.
    var centerStone = $("#board div[data-x='7'][data-y='7'] .stone").addClass("black").parent().attr('data-stone','b');
    var y = 7
    var x = 7
    gameboard = gameboard.replaceAt(parseInt(15*x)+parseInt(x)+parseInt(y), "b");
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
            AIturn = true;
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
        var max = 15
        var mid = x
        gameboard = gameboard.replaceAt(parseInt(15*x)+parseInt(x)+parseInt(y), "b");

    }else{
        //Assign a white stone at x,y
        $("#board div[data-x='"+x+"'][data-y='"+y+"'] .stone").addClass("white").parent().attr('data-stone','w');
        $.each(freeSpaces, function( index, value ) {
        if(value.X == x && value.Y == y)
            freeSpaces[index].value = 'w'
        });
        gameboard = gameboard.replaceAt(parseInt(15*x)+parseInt(x)+parseInt(y), "w");
    }

    //Toggle the current player
    playerBlack = !playerBlack;
    // console.log(gameboard)
    // console.log(x)
    // console.log(y)


    getConnected8(x,y);
    if(AIturn && !gameover)
        getAIMove('b','w',gameboard)
}

function putAIStone(data){
    var response = data.split(',')
    var x = response[0]
    var y = response[1]
    var hval = response[2]
    var player = response[3]
    //Win condition reached
    if(hval > 49000){
        gameover = true;
        $(".square").unbind("click");
        $("#decision").text("Black Wins");
        alert("Black Wins");
    }

    AIturn = false
    clickSquare(y,x,player)
}

function getConnected8(x,y){
    //Ensure concatenation doesnt occur and arithematic does.
    x=parseInt(x)
    y=parseInt(y)

    if(playerBlack)
        if(checkUserWin(x,y)){
            $(".square").unbind("click");
            $("#decision").text("White Wins");
            alert("White Wins");
        }

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

function checkUserWin(x,y){
    originX = x;
    originY = y;

    var northCount = 0;
    var southCount = 0;
    var eastCount = 0;
    var westCount = 0;
    var northeastCount = 0;
    var northwestCount = 0;
    var southeastCount = 0;
    var southwestCount = 0;
    
    
    while(northCount<5 && GetStoneAt(x,y-1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        y=y-1; 
        northCount++;
    }
    while(southCount<5 && GetStoneAt(x,y+1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        y=y+1; 
        southCount++;
    }
    while(eastCount<5 && GetStoneAt(x-1,y) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x=x-1; 
        eastCount++;
    }
    while(westCount<5 && GetStoneAt(x+1,y) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x=x+1; 
        westCount++;
    }
    while(northeastCount<5 && GetStoneAt(x+1,y-1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x = x+1;
        y = y-1;
        northeastCount++;
    }
    while(northwestCount<5 && GetStoneAt(x-1,y-1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x = x-1;
        y = y-1;
        northwestCount++;
    }
    while(southeastCount<5 && GetStoneAt(x+1,y+1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x = x+1;
        y = y+1;
        southeastCount++;
    }
    while(southwestCount<5 && GetStoneAt(x-1,y+1) == 'w' && x >= 0 && x <= 14 && y >= 0 && y <= 14){ 
        x = x-1;
        y = y+1;
        southwestCount++;
    }

console.log("northCount" + northCount);
console.log("southCount" + southCount);
console.log("eastCount" + eastCount);
console.log("westCount" + westCount);
console.log("northeastCount" + northeastCount);
console.log("northwestCount" + northwestCount);
console.log("southeastCount" + southeastCount);
console.log("southwestCount" + southwestCount);

if (northCount == 4 || southCount == 4 || eastCount == 4 || westCount == 4 || northeastCount == 4 || northwestCount == 4 || southeastCount == 4 || southwestCount == 4){
    gameover = true;
    return true;
}
else 
    return false;     
}


function getAIMove(player,opponent,gameboard){
    var currentState = {
            algorithm: "1",
            player:player,
            opponent:opponent,
            depth:"1",
            gamedata:gameboard
        }





        $.ajax({
            url: 'http://gdsouza.pythonanywhere.com/gomoku/game/playMove',
            type: 'post',

            data: JSON.stringify(currentState),
            success: function (data) {
                console.log(data);
                putAIStone(data);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log("Status: " + textStatus); alert("Error: " + errorThrown);
            }

        });
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
