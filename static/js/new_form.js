function onSubmit() {
  $(".inactive").removeClass("inactive");
  $(".error").removeClass("active");
  $("#id_cpf").removeClass("invalid");
}

function verificarInputs(event) {
  event.stopPropagation();
  event.preventDefault();

  var CpfInput = $("#id_cpf");

  if (!CpfInput.val()) {
    CpfInput.addClass("invalid");
    $(".error").addClass("active");
  } else {
    $(".label-float.inactive").removeClass("inactive");
    $(".error").removeClass("active");
    $("#id_cpf").removeClass("invalid");
  }
  if (CpfInput.val() && $("#id_name").val() && $("#id_email").val()) {
    $("#section_1").addClass("inactive");
    $("#section_2").removeClass("inactive");
  }
}
