$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
}

function fillTextArea(filename){
    request = $.ajax({
        url: "uploads/" + filename,
        type: "GET",
        success: function(data){
            $("#srt-content").html(data);
        }
    });
}


function translate(){
     filename = $.urlParam('filename');
     if(filename){
         request = $.ajax({
             url: "translate/" + filename,
             type: "POST",
             success: function(data){
                $("#srt-content").html(data);
            }
        });
     }
}


$( document ).ready(function() {
     filename = $.urlParam('filename');
     if(filename) {
        fillTextArea(filename)
    }
});


