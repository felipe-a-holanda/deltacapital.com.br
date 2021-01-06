
window.onload = function() {
  if (window.jQuery) {  
      // jQuery is loaded  
      disableError();
  }
}


function disableError(){
  var inputs = $(".label-float > input");
  $(".label-float > input").on("change paste keyup", function() {
    $(this).removeClass("invalid");
    $(this).siblings('.error').removeClass('active');
  });
}


function verificarInputs(event) {
  event.stopPropagation();
  event.preventDefault();

  var CpfInput = $("#id_cpf");
  var activeDiv = $(".label-float:not(.inactive)");
  

  $.each(activeDiv, function(index, Div) {
    var input = $(Div).children('input').first();
    var erroMsg =  $(Div).children('.error').first();

    if (!input.val()) {
      $(input).addClass("invalid");
      $(erroMsg).addClass("active");
    } else {
      $(input).removeClass("invalid");
      $(erroMsg).removeClass("active");
    }
  });

  if(CpfInput.val()){
    $("#section_1 .label-float.inactive").removeClass("inactive");
  }
  
  /*Se todos três campos da primeira sessão foram preenchidos ativa a seção 2 e ativa seus inputs*/
  if (CpfInput.val() && $("#id_name").val() && $("#id_email").val()) {
    $("#section_1").addClass("inactive");
    $("#section_2").removeClass("inactive");
    $("#section_2 .label-float.inactive").removeClass("inactive");
  }
}

