function onSubmit() {
  $(".inactive").removeClass("inactive");
  $("#cpf").removeClass("invalid");
}

function verificarInputs(event) {
  var inputs = $("#cpf");
  event.stopPropagation();
  event.preventDefault();

  //console.log(inputs);
  if (!inputs.val()) {
    inputs.addClass("invalid");
    $(".error").addClass("active");
  } else {
    onSubmit();
    $(".error").removeClass("active");
  }
}
