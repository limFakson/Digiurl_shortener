$.ajaxSetup({
  headers: {
    "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content"),
  },
});


$("#longurl").val("")

$(document).on("click", ".cursor-pointer", function (e) {
  console.log("rebuild");
});

function convert() {
  var longurl = $("#longurl").val();
  console.log(longurl);
  $.ajax({
    type: "POST",
    url: "/short/api/url",
    data: {
      url: longurl,
    },

    success: function (data) {
      console.log(data["shorturl"]);
      $('#short').text("");
      var shorturl = data["shorturl"];
      var htmltext ='<p id="shorturl" class="inline-block pr-4 underline text-[#0d609b] cursor-copy">' + shorturl + "</p>";
      var icon = '<i class="fa-solid fa-copy"></i>'
    
      $('#short').append(htmltext);
      $('#copy').append(icon)
      $("#longurl").val("")
    },
  });
}


$(document).on('click', "#copy", function(e){
    var temp = $('<input/>')
    $("body").append(temp)
    temp.val($('#short').text()).select()
    document.execCommand("copy")
    temp.remove()
    console.log("copied")
    var alert = '<p class="underline text-base pt-2" id="alert">copied!!😎</p>'
    $('.short').append(alert)
    
    setTimeout(() => {
        const alert = document.getElementById('alert');
        if (alert) {
            alert.style.transition = "ease-in-out 3000s"
            alert.style.display = 'none';
        }
    }, 1000);
})
