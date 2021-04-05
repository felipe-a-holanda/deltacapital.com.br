
function TestaCPF(inputCPF) {
  var strCPF = inputCPF.replace(/[\.\-]+/g, '');  
  var Soma;
  var Resto;
  Soma = 0;
if (strCPF == "00000000000"||
        strCPF == "11111111111" ||
        strCPF == "22222222222" ||
        strCPF == "33333333333" ||
        strCPF == "44444444444" ||
        strCPF == "55555555555" ||
        strCPF == "66666666666" ||
        strCPF == "77777777777" ||
        strCPF == "88888888888" ||
        strCPF == "99999999999" ) return false;

for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
Resto = (Soma * 10) % 11;

  if ((Resto == 10) || (Resto == 11))  Resto = 0;
  if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

Soma = 0;
  for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
  Resto = (Soma * 10) % 11;

  if ((Resto == 10) || (Resto == 11))  Resto = 0;
  if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
  return true;
}

window.onload = function() {
  if (window.jQuery) {  
      // jQuery is loaded ;
      disableError();
      updatePercentage();
      // on browser resize...
      $(window).resize(function() {
        moveProgressBar();
      });
  }
}


function disableError(){
  $(".label-float > input").on("change paste keyup", function() {
    $(this).removeClass("invalid");
    $(this).siblings('.error').removeClass('active');
  });
}

function verificarInputs(event) {
  event.stopPropagation();
  event.preventDefault();

  var CpfInput = $("#id_cpf");
  var activeSection = $('.section:not(.inactive)');  
  var activeDiv = $(activeSection).children(".label-float:not(.inactive)");

  const sectionName = activeSection.attr('id');
  var inactiveDivs = $(activeSection).children(".label-float.inactive");
  var sectionNumber = sectionName.slice(-1);

  var hasInvalid = false;
  
  //se não tem inativos na sessão
  // a cada active input não preenchido 
  // se não tiver não prenchido chama próxima seção

  $.each(activeDiv, function(index, Div) {
    var input = $(Div).children('input, select').first();
    var erroMsg =  $(Div).children('.error').first();

    if (!input.val()) {
      $(input).addClass("invalid");
      $(erroMsg).addClass("active");
      hasInvalid = true;
    } else {
      $(input).removeClass("invalid");
      $(erroMsg).removeClass("active");
    }
  });

  //Generalisar?
  if(CpfInput.val()){
    if(TestaCPF(CpfInput.val())){
      $(CpfInput).removeClass("invalid");
      $('.cpf-error').removeClass("active");
      $("#section_1 .label-float.inactive").removeClass("inactive");
    }
    else{
      $(CpfInput).addClass("invalid");
      $('.cpf-error').addClass("active");
    }
  }
  
  // Se não tiver Divs inputs inativos e se não tiver nenhum inválido
  // Vai para próxima section;  
  if(inactiveDivs.length === 0 && !hasInvalid){
    // Senão for a ultima sessão vai para próxima
    // Se for adiciona o botão de submeter o form
    if(sectionNumber < $('.section').length ){
      nextSection(activeSection, sectionNumber);
    }
    if(sectionNumber == ($('.section').length - 1) ){
      $('#next_button').addClass('inactive');
      $('#submit_button').removeClass('inactive');
    }
  }
}

//Validação do form cdc
function validateForm() {
  var activeSection = $('form:not(.inactive)');  
  var activeDivs = $(activeSection).children(".label-float:not(.inactive)");

  $.each(activeDivs, function(index, Div) {
    var input = $(Div).children('input:not([readonly]), select').first();
    var erroMsg =  $(input).siblings('.error').first();

    if (!input.val()) {
      $(input).addClass("invalid");
      $(erroMsg).addClass("active");
    } else {
      $(input).removeClass("invalid");
      $(erroMsg).removeClass("active");
    }
  });
} 

// A partir do nome da sessão ativa, calcula o nome da próxima e a ativa
function nextSection(activeSection, sectionNumber){
  sectionNumber = Number(sectionNumber) + 1;
  const nextSectionName = "section_" + sectionNumber;
  const nexSectionDiv = $('#' + nextSectionName);

  $(activeSection).addClass("inactive");
  $(nexSectionDiv).removeClass("inactive");
  $(nexSectionDiv).children('.label-float.inactive').removeClass("inactive");
  $("#back_button").removeClass('inactive');
  updatePercentage();
}

// Verificar se é a primeira
function backSection(){
  const activeSection = $('.section:not(.inactive)');
  const sectionName = activeSection.attr('id');
  var sectionNumber = sectionName.slice(-1);
  sectionNumber = Number(sectionNumber) - 1;
  const backSectionName = "section_" + sectionNumber;
  const backSectionDiv = $('#' + backSectionName);

  $(activeSection).addClass("inactive");
  $(backSectionDiv).removeClass("inactive");
  if(sectionNumber === 1){
    $("#back_button").addClass('inactive');
  }
  
  $('#submit_button').addClass('inactive');
  $('#next_button').removeClass('inactive');

  updatePercentage();
}

/*Progress bar*/


// SIGNATURE PROGRESS
function moveProgressBar() {
    var getPercent = ($('.progress-wrap').data('progress-percent'));
    var getProgressWrapWidth = $('.progress-wrap').width();
    var progressTotal = getPercent * getProgressWrapWidth;
    var animationLength = 1000;
    
    // on page load, animate percentage bar to data percentage length
    // .stop() used to prevent animation queueing
    $('.progress-bar').stop().animate({
        left: progressTotal
    }, animationLength);
}

function updatePercentage(){
  const sectionNumber = $('.section:not(.inactive)').attr('id').slice(-1);  
  const totalSection = $('.section').length;
  const percentage = (sectionNumber / (totalSection+1));
  $("#progress-div").attr('data-progress-percent', percentage);
  $("#progress-div").data('progress-percent', percentage);
  moveProgressBar();
}