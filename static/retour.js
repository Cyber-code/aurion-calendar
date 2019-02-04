$("#send_message").click(function (e) { 
    e.preventDefault();
    var email = $('#email').val();
    var message = $('#message').val();
    $.post("/send_error/",{'email':email,'message':message}).done(function(resp){
        alert('Message envoyé ! Merci !');
    })
    .fail(function(xhr, status, error){
        if(xhr.status == 417){
            $("#boxAlert").toggleClass('hide',false);
            $("#MessageAlert").text("L'adresse email et le message ne doit pas être vide !");
            var time = setInterval(function () {
                $("#boxAlert").toggleClass('hide',true);
                clearInterval(time);
            }, 3000);
        }
    });
});