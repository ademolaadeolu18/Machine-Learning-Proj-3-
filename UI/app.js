Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/image_classifier";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            /* 
            Below is a sample response if you have two faces in an image lets say Zlatan and    Sharapova together.
            Most of the time if there is one person in the image you will get only one element in below array
            data = [
                {
                    class: "Zlatan_Ibrahimovic",
                    confidence_level: [1.05, 12.67, 22.00, 4.5, 91.56],
                    class_dictionary: {
                        Dwayne_Johnson: 0,
                        Lionel_Messi: 1,
                        Maria_Sharapova: 2,
                        Serena_Williams: 3,
                        Zlatan_Ibrahimovic: 4
                    }
                },
                {
                    class: "Maria_Sharapova",
                    confidence_level: [7.02, 23.7, 52.00, 6.1, 1.62],
                    class_dictionary: {
                        Dwayne_Johnson: 0,
                        Lionel_Messi: 1,
                        Maria_Sharapova: 2,
                        Serena_Williams: 3,
                        Zlatan_Ibrahimovic: 4
                    }
                }
            ]
            */
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let players = ["Dwayne_Johnson", "Lionel_Messi", "Maria_Sharapova", "Serena_Williams", "Zlatan_Ibrahimovic"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].confidence_level);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.Celeb}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.confidence_level[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});