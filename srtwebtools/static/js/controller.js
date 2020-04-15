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

     if(filename){
         let from_lang = $(".dropdown[translate-option='from']").children(".btn").val();
         if(!from_lang){
            alertErrorMessage("Please specify a language to translate from.");
            return false;
         }
         let to_lang = $(".dropdown[translate-option='to']").children(".btn").val();
         if(!to_lang){
            alertErrorMessage("Please specify a language to translate to.");
            return false;
         }

         var refreshIntervalId = setInterval(function(){requestAndSetProgress()}, 500);
         request = $.ajax({
             url: "translate/" + filename,
             type: "POST",
             dataType : "json",
             contentType: "application/json; charset=utf-8",
             data: JSON.stringify({
                from_lang : from_lang,
                to_lang : to_lang,
                overwrite : $("#overwrite-translation").hasClass("active")
             }),
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


function set_from_to_languages(dropdown, value){

    let dropdownButton = dropdown.children(".btn");
    dropdownButton.val(value);

    dropdownButton.filter(function(){
        return dropdown.is("[translate-option='from']")
    }).html("From Language: " + dropdownButton.val());
    dropdownButton.filter(function(){
        return dropdown.is("[translate-option='to']")
    }).html("To Language: " + dropdownButton.val());
}

function set_default_languages(){
    request = $.ajax({
        url: "default_languages",
        type: "GET",
        success: function(data){
             set_from_to_languages($(".dropdown[translate-option='from']"), data.from_lang);
             set_from_to_languages($(".dropdown[translate-option='to']"), data.to_lang);
        }
    });
}

function add_languages(){
    request = $.ajax({
        url: "languages",
        type: "GET",
        success: function(data){
            let language_dropdown = $(".dropdown[translate-option]");
            $.each(data.languages, function(index, language){
                language_dropdown.children(".dropdown-menu").append('<div class="dropdown-item">' + language + '</div>');
            });
            $('.dropdown-item').click(function(event){
                set_from_to_languages($(this).closest(".dropdown"), $(this).html());
            });
            set_default_languages();
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


