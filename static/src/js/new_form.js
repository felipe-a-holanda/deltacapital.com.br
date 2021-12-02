/*!
 * currency.js - v2.0.4
 * http://scurker.github.io/currency.js
 *
 * Copyright (c) 2021 Jason Wilson
 * Released under MIT license
 */

'use strict';


var defaults = {
  symbol: 'R$',
  separator: '.',
  decimal: ',',
  errorOnInvalid: false,
  precision: 2,
  pattern: '!#',
  negativePattern: '-!#',
  format: format,
  fromCents: false
};

var round = function round(v) {
  return Math.round(v);
};

var pow = function pow(p) {
  return Math.pow(10, p);
};

var rounding = function rounding(value, increment) {
  return round(value / increment) * increment;
};

var groupRegex = /(\d)(?=(\d{3})+\b)/g;
var vedicRegex = /(\d)(?=(\d\d)+\d\b)/g;
/**
 * Create a new instance of currency.js
 * @param {number|string|currency} value
 * @param {object} [opts]
 */

function currency(value, opts) {
  var that = this;

  if (!(that instanceof currency)) {
    return new currency(value, opts);
  }

  var settings = Object.assign({}, defaults, opts),
      precision = pow(settings.precision),
      v = parse(value, settings);
  that.intValue = v;
  that.value = v / precision; // Set default incremental value

  settings.increment = settings.increment || 1 / precision; // Support vedic numbering systems
  // see: https://en.wikipedia.org/wiki/Indian_numbering_system

  if (settings.useVedic) {
    settings.groups = vedicRegex;
  } else {
    settings.groups = groupRegex;
  } // Intended for internal usage only - subject to change


  this.s = settings;
  this.p = precision;
}

function parse(value, opts) {
  var useRounding = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : true;
  var v = 0,
      decimal = opts.decimal,
      errorOnInvalid = opts.errorOnInvalid,
      decimals = opts.precision,
      fromCents = opts.fromCents,
      precision = pow(decimals),
      isNumber = typeof value === 'number',
      isCurrency = value instanceof currency;

  if (isCurrency && fromCents) {
    return value.intValue;
  }

  if (isNumber || isCurrency) {
    v = isCurrency ? value.value : value;
  } else if (typeof value === 'string') {
    var regex = new RegExp('[^-\\d' + decimal + ']', 'g'),
        decimalString = new RegExp('\\' + decimal, 'g');
    v = value.replace(/\((.*)\)/, '-$1') // allow negative e.g. (1.99)
    .replace(regex, '') // replace any non numeric values
    .replace(decimalString, '.'); // convert any decimal values

    v = v || 0;
  } else {
    if (errorOnInvalid) {
      throw Error('Invalid Input');
    }

    v = 0;
  }

  if (!fromCents) {
    v *= precision; // scale number to integer value

    v = v.toFixed(4); // Handle additional decimal for proper rounding.
  }

  return useRounding ? round(v) : v;
}
/**
 * Formats a currency object
 * @param currency
 * @param {object} [opts]
 */


function format(currency, settings) {
  var pattern = settings.pattern,
      negativePattern = settings.negativePattern,
      symbol = settings.symbol,
      separator = settings.separator,
      decimal = settings.decimal,
      groups = settings.groups,
      split = ('' + currency).replace(/^-/, '').split('.'),
      dollars = split[0],
      cents = split[1];
  return (currency.value >= 0 ? pattern : negativePattern).replace('!', symbol).replace('#', dollars.replace(groups, '$1' + separator) + (cents ? decimal + cents : ''));
}

currency.prototype = {
  /**
   * Adds values together.
   * @param {number} number
   * @returns {currency}
   */
  add: function add(number) {
    var intValue = this.intValue,
        _settings = this.s,
        _precision = this.p;
    return currency((intValue += parse(number, _settings)) / (_settings.fromCents ? 1 : _precision), _settings);
  },

  /**
   * Subtracts value.
   * @param {number} number
   * @returns {currency}
   */
  subtract: function subtract(number) {
    var intValue = this.intValue,
        _settings = this.s,
        _precision = this.p;
    return currency((intValue -= parse(number, _settings)) / (_settings.fromCents ? 1 : _precision), _settings);
  },

  /**
   * Multiplies values.
   * @param {number} number
   * @returns {currency}
   */
  multiply: function multiply(number) {
    var intValue = this.intValue,
        _settings = this.s;
    return currency((intValue *= number) / (_settings.fromCents ? 1 : pow(_settings.precision)), _settings);
  },

  /**
   * Divides value.
   * @param {number} number
   * @returns {currency}
   */
  divide: function divide(number) {
    var intValue = this.intValue,
        _settings = this.s;
    return currency(intValue /= parse(number, _settings, false), _settings);
  },

  /**
   * Takes the currency amount and distributes the values evenly. Any extra pennies
   * left over from the distribution will be stacked onto the first set of entries.
   * @param {number} count
   * @returns {array}
   */
  distribute: function distribute(count) {
    var intValue = this.intValue,
        _precision = this.p,
        _settings = this.s,
        distribution = [],
        split = Math[intValue >= 0 ? 'floor' : 'ceil'](intValue / count),
        pennies = Math.abs(intValue - split * count),
        precision = _settings.fromCents ? 1 : _precision;

    for (; count !== 0; count--) {
      var item = currency(split / precision, _settings); // Add any left over pennies

      pennies-- > 0 && (item = item[intValue >= 0 ? 'add' : 'subtract'](1 / precision));
      distribution.push(item);
    }

    return distribution;
  },

  /**
   * Returns the dollar value.
   * @returns {number}
   */
  dollars: function dollars() {
    return ~~this.value;
  },

  /**
   * Returns the cent value.
   * @returns {number}
   */
  cents: function cents() {
    var intValue = this.intValue,
        _precision = this.p;
    return ~~(intValue % _precision);
  },

  /**
   * Formats the value as a string according to the formatting settings.
   * @param {boolean} useSymbol - format with currency symbol
   * @returns {string}
   */
  format: function format(options) {
    var _settings = this.s;

    if (typeof options === 'function') {
      return options(this, _settings);
    }

    return _settings.format(this, Object.assign({}, _settings, options));
  },

  /**
   * Formats the value as a string according to the formatting settings.
   * @returns {string}
   */
  toString: function toString() {
    var intValue = this.intValue,
        _precision = this.p,
        _settings = this.s;
    return rounding(intValue / _precision, _settings.increment).toFixed(_settings.precision);
  },

  /**
   * Value for JSON serialization.
   * @returns {float}
   */
  toJSON: function toJSON() {
    return this.value;
  }
};

module.exports = currency;

/**end currency
   */

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

  var input = $("#id_valor_de_entrada");
  var actId = $("#id_valor_financiado");

  var hasInvalid = false;
  if(currency(input.val()).value >= currency($("#id_valor_do_veiculo").val()).value){
      $(actId.addClass("invalid"));
      hasInvalid = true;
      console.log(currency(input.val()).value,">=",currency($("#id_valor_do_veiculo").val()).value);
     } else {
      $(input).removeClass("invalid");
     }
  
  $.each(activeDivs, function(index, Div) {
    var input = $(Div).children('input:not([readonly]):not([style*="display: none"]), select').first();
    var erroMsg =  $(input).siblings('.error').first();
    // se o input não for outras rendas e telefone fixo add msg de error
    if((input.attr("id") !== "id_outras_rendas") && (input.attr("id") !== "id_telefone_fixo_da_empresa")){
    
      if (input.is(":visible") && !input.val()) {
        $(input).addClass("invalid");
        console.log(input);
        $(erroMsg).addClass("active");
        hasInvalid = true;
      } else {
        $(input).removeClass("invalid");
        $(erroMsg).removeClass("active");
      }

    }
  });
  //verificar em que pagina esta
    //pegar a url
    var url = window.location.href;
    // pegar a ultima substring e verificar se é a 6
    var list = url.split('/');
    var pag = list[5];
  // se for na pag 6 chama o validateAnoFabric
    if(pag == '6'){
      hasInvalid = validateAnoFabric()
    }
    if(!hasInvalid){
      document.getElementById("proposta-financiamento").submit();
    }

}; 

function validateAnoFabric(){
  var input = $("#id_ano_do_modelo");
  var actiId = $("#id_ano_de_fabricacao");
  var hasInvalid = false;
  
  if(input.val() < $("#id_ano_de_fabricacao").val()){
    $(input.addClass("invalid"));
    hasInvalid = true;
    alert("O Ano do Modelo não pode ser menor que ano de fabricação.");
  } else {
    $(input).removeClass("invalid");
    }
  return hasInvalid;
};

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