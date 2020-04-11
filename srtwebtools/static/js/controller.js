$.urlParam = function(name){
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
}

$(function(){
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide();
    });
});


function fillTextArea(filename){
    request = $.ajax({
        url: "uploads/" + filename,
        type: "GET",
        success: function(data){
            $("#srt-content").html(data);
        }
    });
}

function percentfloatToString(percentfloat){
    return Math.round(percentfloat*100*100)/100 + "%";
}

function setProgress(percentfloat){
    let percent = percentfloatToString(percentfloat);
    let progress = $(".progress-bar");
    progress.css("width", percent);
    progress.html(percent);
}

function requestAndSetProgress(){
    request = $.ajax({
        url: "translation_status",
        type: "GET",
        success: function(data){
            setProgress(data.progress);
        }
    });
}

function alertErrorMessage(message){
    $("#errormessage").html('<strong>Error:</strong> ' + message);
    $(".alert").alert();
	$(".alert").fadeIn('slow');
}

function translate(){
     filename = $.urlParam('filename');
     var refreshIntervalId = setInterval(function(){requestAndSetProgress()}, 500);

     if(filename){
         request = $.ajax({
             url: "translate/" + filename,
             type: "POST",
             success: function(data){
                $("#srt-modified-content").html(data.content);
                setProgress(1);
                $("#downloadbutton").prop('disabled', false);
                $('#downloadfilename').val(data.filename);
             },
			 error: function(xhr, status, error) {
                try {
                    data = JSON.parse(xhr.responseText);
                    if(data.error === 'LockError'){
                        let percent = percentfloatToString(data.value.progress);
                        alertErrorMessage("Translator is busy at: " + percent);
                    }
                    else if (data.error === 'ConnectionError'){
                        alertErrorMessage("A connection error occured, please try again.");
                    }
                }
                catch(e) {
                    console.error(error);
                }

			 },
             complete: function(){
                clearInterval(refreshIntervalId);
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
     let percent = Math.round(0.12345*100*100)/100 + "%";
     filename = $.urlParam('filename');
     if(filename) {
        fillTextArea(filename)
    }
});


