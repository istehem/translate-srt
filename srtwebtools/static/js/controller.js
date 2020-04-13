$.urlParam = function(name){
    try {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        return results[1] || 0;
    }
    catch(e){
        return 0;
    }
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
            $("#srt-content").html(encode(data));
            $(".translate-btn").prop('disabled', false);
        },
        error: function(xhr, status, error) {
            try {
                data = JSON.parse(xhr.responseText);
                if (data.error === 'FileNotFoundError'){
                    alertErrorMessage("File " + data.value.filename + " not found or not valid, please specify another file.");
                }
                if (data.error === 'UnicodeDecodeError'){
                    alertErrorMessage("File name invalid, please specify another file.");
                }
            }
            catch {
                console.error(error);
            }
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

function encode(text){
    return $('<div>').text(text).html();
}

function alertError(){
    $(".alert").alert();
    $(".alert").fadeIn('slow');
}

function alertErrorMessage(message){
    $("#errormessage").html('<strong>Error:</strong> ' + encode(message));
    $("#errormessage").html(html);
    alertError();
}

function alertErrorMessage(message, id, linktext){
    let html = encode(message) + '<a id="' + id  + '" href="#">' + encode(linktext) + "</a>";
    $("#errormessage").html(html);
    alertError();
}

function translate(){
     filename = $.urlParam('filename');
     var refreshIntervalId = setInterval(function(){requestAndSetProgress()}, 500);

     if(filename){
         request = $.ajax({
             url: "translate/" + filename,
             type: "POST",
             success: function(data){
                $("#srt-modified-content").html(encode(data.content));
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
                        let tryAgain = "tryagain";
                        alertErrorMessage("A connection error occured, ", tryAgain, "please try again");
                        $('#' + tryAgain).click(function() {
                            $(this).closest(".alert").hide();
                            translate();
                            return false;
                        });
                    }
                    else if (data.error === 'FileNotFoundError'){
                        alertErrorMessage("File " + data.value.filename + " not found or not valid, please specify another file.");
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
     else {
        alertErrorMessage("Please select a file.");
     }
}

function download(){
    let filename = $("#downloadfilename").val();
    if(filename){
        window.open("downloadtranslation/" + filename, '_blank');
    }
}

function add_language_item(dropdown, language){
    dropdown.parent().children('.dropdown-menu').append('<a class="dropdown-item" href="#">' + language + '</a>');
}

function add_languages(){
    request = $.ajax({
        url: "languages",
        type: "GET",
        success: function(data){
            let to_languages = $("#to-language");
            let from_languages = $("#from-language");
            $.each(data.languages, function(index, language){
                add_language_item(to_languages, language);
                add_language_item(from_languages, language);
            });
        }
    });
}

$( document ).ready(function() {
     filename = $.urlParam('filename');
     if(filename) {
        fillTextArea(filename);
    }
    $("#overwrite-translation").on("change", function(){
        $(this).button('toggle');
        if($(this).hasClass("active")){
            //$(this).closest('.btn').addClass('fa fa-check');
            $(this).closest('.btn').addClass('checkbox-active');
        }
        else{
            //$(this).closest('.btn').removeClass('fa fa-check');
            $(this).closest('.btn').removeClass('checkbox-active');
        }
    });
    add_languages();
});


