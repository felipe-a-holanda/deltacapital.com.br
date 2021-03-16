
// var Inputmask = require('inputmask');
import Inputmask from 'inputmask';

$(document).ready(function(){


  var mask_moeda = {
                'alias': 'numeric',
                'groupSeparator': '.',
                'autoGroup': true,
                'digits': 2,
                'radixPoint': ",",
                'digitsOptional': true,
                'allowMinus': false,
                'prefix': 'R$ ',
                'placeholder': '',
                'rightAlign': false

  };

  var mask_cpf ={  "mask":"999.999.999-99", 'placeholder': '___.___.___-__'}
  var mask_cnpj ={ "mask":"99.999.999/9999-99", 'placeholder': '__.___.___/____-__'}
  var mask_data ={"alias":"datetime", 'inputFormat': 'dd/mm/yyyy', 'displayFormat':'dd/mm/aaaa', }
  var mask_cep ={"mask":"99999-999", 'placeholder': '_____-___'}
  var mask_celular ={ "mask":"(99) [9]9999-9999", 'placeholder': ''}
  var mask_telefone ={ "mask":"(99) 9999-9999", 'placeholder': ''}
  var mask_email ={ "alias": "email"}
  //var mask_email ={ "mask": ".*@.*"}
  var mask_numero ={ "alias": "numeric", "rightAlign": false,}


  Inputmask(mask_moeda).mask("input.moeda");
  Inputmask(mask_cpf).mask("input.cpf");
  Inputmask(mask_cnpj).mask("input.cnpj");
  Inputmask(mask_data).mask("input.data");
  Inputmask(mask_cep).mask("input.cep");
  Inputmask(mask_celular).mask("input.celular");
  Inputmask(mask_telefone).mask("input.telefone");
  Inputmask(mask_email).mask("input.email");
  Inputmask(mask_numero).mask("input.numero");
});