$('#btnLog').click(function(){
    //$('#btnLog').prop( "disabled", true );
    $('#boxMenu').toggleClass('hide',false);
    $('#TitreInfo').text("Récupération de l'emploi du temps");
    var passw = $('#password').val();
    var user = $('#email').val();
    var DateS = $('.active').attr('value');
    //console.log(DateS);
    $('.loginForm').toggleClass('hide',true);
    $.post("/connexion/",{'pass':passw,'user':user,'date':DateS}).done(function(resp){
        console.log(resp);
        if (resp.status == "error") {
            console.log('ok');
            $('.loginForm').toggleClass('hide',false);
            $('#boxMenu').toggleClass('hide',true);
        }else{
            $('#boxMenu').html(resp.data);
            call_planning();
        }
    })
    .fail(function(xhr){
        console.log(xhr);
        if(xhr.status == 500){
            showError("Erreur interne ! Envoyer moi un message sur l'adresse d'erreur svp !!");
        }
        if(xhr.status == 418){
            err = xhr.responseJSON;
            showError(err.status);
        }
        $('#btnLog').prop( "disabled", false );
        $('.loginForm').toggleClass('hide',false);
        $('#TitreInfo').text("Connexion");
        $('#boxMenu').html(null);
        $('#boxMenu').toggleClass('hide',true);
    });
  });

  function showError(text){
    $("#boxAlert").toggleClass('alertHide',false);
    if (text == "NotCoPass") {
        text = "La combinaison mot de passe/identifiant est mauvaise";
    }
    if (text == "NotCoNull") {
        text = "Vous devez remplir tous les champs";
    }
    
    $("#MessageAlert").text(text);
    var time = setInterval(function () {
        $("#boxAlert").toggleClass('alertHide',true);
        clearInterval(time);
    }, 5000);
  }

function call_planning(){
    $.post("/planning/",{}).done(function(resp){
        if (resp.status == "error") {
            $('.loginForm').toggleClass('hide',false);
            $('#boxMenu').toggleClass('hide',true);
        }
        $('#boxMenu').html(resp.data);
        create_calendrier();
    })
    .fail(function(xhr){
        $('#btnLog').prop( "disabled", false );
        //console.log(xhr);
        if(xhr.status = 500){
            showError("Erreur interne ! Envoyer moi un message sur l'adresse d'erreur svp !!");
            $('.loginForm').toggleClass('hide',false);
            $('#TitreInfo').text("Connexion");
            $('#boxMenu').toggleClass('hide',true);
        }
    });
}

function create_calendrier(){
    $.post("/create_calen/",{}).done(function(resp){
        if (resp.status == "error") {
            $('.loginForm').toggleClass('hide',false);
            $('#boxMenu').toggleClass('hide',true);
        }
        $('#boxMenu').html(resp.data);
    })
    $('#btnLog').prop( "disabled", false );
        //console.log(xhr);
        if(xhr.status = 500){
            showError("Erreur interne ! Envoyer moi un message sur l'adresse d'erreur svp !!");
            $('.loginForm').toggleClass('hide',false);
            $('#TitreInfo').text("Connexion");
            $('#boxMenu').toggleClass('hide',true);
        }
}

$("li").each(function() {
    $(this).click(function(){
        $('.active').toggleClass('changement',true);
        $('.changement').toggleClass('active',false);
        $('.inactive').toggleClass('active',true);
        $('.active').toggleClass('inactive',false);
        $('.changement').toggleClass('inactive',true);
        $('.inactive').toggleClass('changement',false);
    })
  });


