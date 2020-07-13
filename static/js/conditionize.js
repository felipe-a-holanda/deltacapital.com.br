/* * * * * * * * * * * * * * * * * *
* Show/hide fields conditionally
* * * * * * * * * * * * * * * * * */
(function($) {
  $.fn.conditionize = function(options){

     var settings = $.extend({
        hideJS: true
    }, options );

    $.fn.showOrHide = function(listenTo, listenFor, $section) {
      if ($(listenTo).is('select, input[type=text]') && $(listenTo).val() == listenFor ) {
        $section.slideDown();
      }
      else if ($(listenTo + ":checked").val() == listenFor) {
        $section.slideDown();
      }
      else {
        $section.slideUp();
      }
    }

    return this.each( function() {
      var listenTo = "[name=" + $(this).data('cond-option') + "]";
      var listenForData = $(this).data('cond-value');
      if (listenForData) {
        var listenForList = listenForData.split(' ')
        console.log(listenForList);
      }
      else {
         listenForList = [];
      }
      var $section = $(this);

      //Set up event listener
      listenForList.forEach(function(listenFor, index, array){
        console.log("listenFor:",listenFor);
        console.log(listenTo, listenFor, $section);
        $(listenTo).on('change', function() {
            $.fn.showOrHide(listenTo, listenFor, $section);
          });

      })


//      $(listenTo).on('change', function() {
//        $.fn.showOrHide(listenTo, listenFor, $section);
//      });

      //If setting was chosen, hide everything first...
      if (settings.hideJS) {
        $(this).hide();
      }
      //Show based on current value on page load
      //$.fn.showOrHide(listenTo, listenFor, $section);


      console.log("listenForList",listenForList);

      listenForList.forEach(function(listenFor, index, array){
        $.fn.showOrHide(listenTo, listenFor, $section);

      })



    });
  }
}(jQuery));

 $('.conditional').conditionize();