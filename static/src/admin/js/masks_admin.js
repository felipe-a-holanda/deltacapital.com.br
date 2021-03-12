
//var Inputmask = require('inputmask');
//import Inputmask from 'inputmask';

jQuery(document).ready(function(){




  var mask_cpf ={  "mask":"999.999.999-99", 'placeholder': '___.___.___-__'}

  Inputmask(mask_cpf).mask("#id_cpf");
});