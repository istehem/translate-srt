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
                $("#srt-modified-content").html(data.content);
                let progress = $(".progress-bar");
                progress.css("width", "100%");
                progress.html("100%");
                $("#downloadbutton").prop('disabled', false);
                $('#downloadfilename').val(data.filename);
            }
        });
     }
}

function download(){
    let filename = $("#downloadfilename").val();
    if(filename){
        window.open("downloadtranslation/" + filename, '_blank');
    }
}


$( document ).ready(function() {
     filename = $.urlParam('filename');
     if(filename) {
        fillTextArea(filename)
    }
});


