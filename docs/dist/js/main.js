window.addEventListener("dragover",function(e){
e = e || event;
e.preventDefault();
},false);

window.addEventListener("drop",function(e){
e = e || event;
e.preventDefault();
},false);

var dragCounter = 0;
var ENDPOINT_LOCATION = String(window.location).includes("nbsharing.com") ? "https://europe-west1-sacred-garden-192600.cloudfunctions.net" : ""

$(document).ready(function() {
$('#dropzone').on('dragenter', function(e){
    dragCounter++
    e.preventDefault()
    $(this).addClass('active');
});

$('#dropzone').on('dragleave', function(e){
    dragCounter--;
    e.preventDefault()
    if (dragCounter === 0) {
    $(this).removeClass('active');
    }
});

$('#dropzone').on('dragend', function(e){
    e.preventDefault()
});

$('#dropzone').on('drop', function(e){
    e.preventDefault();
    dragCounter = 0;
    $(this).removeClass('active');
    $("#notebookFileUpload")[0].files = e.originalEvent.dataTransfer.files
    $("#uploadButton").click()
});

$("#notebookFileUpload").on("change", function() {
    var filename = $("#notebookFileUpload")[0].files[0].name;
    $("#notebookFileUploadLabel").text(filename)
})
$("#uploadButton").on("click", function() {
    if ($("#notebookFileUpload")[0].files.length === 0) {
    return;
    }
    $("#notebookLink").fadeTo("fast", 0)
    $(".overlay").removeClass("d-none")
    var formData = new FormData();
    formData.append("notebook", $("#notebookFileUpload")[0].files[0])
    fetch(ENDPOINT_LOCATION + "/nbconvert", {
    body: formData,
    method: "post"
    }).then(function(response) {
    $(".overlay").addClass("d-none")
    return response.text().then(function(text) {
        $("#notebookFileUpload").val("")
        $("#notebookFileUploadLabel").text("Select a notebook")
        $("#notebookLink").val(text)
        $("#notebookLink").fadeTo("slow", 1)
    })
    })
})

})