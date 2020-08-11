function get_data(data, field){
    return data[field].toUpperCase();
};

function get_cep(cep, n){
  url = 'https://viacep.com.br/ws/'+cep+'/json/'
  jQuery.getJSON(url,function(data){
  console.log(data);

    jQuery('.autofill__rua_'+n).val(get_data(data, 'logradouro'));
    jQuery('.autofill__bairro_'+n).val(get_data(data, 'bairro'));
    jQuery('.autofill__cidade_'+n).val(get_data(data, 'localidade'));
    jQuery('.autofill__uf_'+n).val(get_data(data, 'uf'));


  });
};


jQuery('.autofill__cep_1').blur(function(){

  cep = this.value.replace(/\D/g,'');
  get_cep(cep, 1);

});

jQuery('.autofill__cep_2').blur(function(){

  cep = this.value.replace(/\D/g,'');
  get_cep(cep, 2);

});
