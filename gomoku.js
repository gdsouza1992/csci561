

$(document).ready(function(){
    for (i = 0; i <15; i++) { 
        for (j = 0; j <15; j++){
            $("#board").append("<div class=square>("+i+","+j+")<div>")    
        }
    }    
});
