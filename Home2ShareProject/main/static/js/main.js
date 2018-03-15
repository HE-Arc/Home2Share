enabled_buttons = null;

$('.rating-block button').hover( function(event){
  enabled_buttons = $('.rating-block button.btn-warning');
  $('.rating-block button').removeClass('btn-warning btn-grey');
  $(this).addClass('btn-warning');
  $(this).prevAll().addClass('btn-warning');
  $(this).nextAll().addClass('btn-grey');
}, function(event){
  if(enabled_buttons){
    $('.rating-block button').removeClass('btn-warning btn-grey');
    $('.rating-block button').addClass('btn-grey');
    $(enabled_buttons).addClass('btn-warning').removeClass('btn-grey');
  }

});

$('.rating-block button').on('click', function(event){
  event.preventDefault();
  var frm = $('#form_eval');
  var button = $(this);
  var stars = button.attr('data-value');
  enabled_buttons = null;
  // alert(button.attr('data-value'));
  $.ajax({
    type: frm.attr('method'),
    url: frm.attr('action'),
    data: {
      house_id : frm.attr('data-id'),
      house_slug : frm.attr('data-slug'),
      stars : stars,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success : function(response){
      // alert('ajax good ' + response);
      if(response['change_validated']){

        // Updates corresponding class to button
        $('.rating-block button').each( function(index){
          $(this).removeClass('btn-warning btn-grey');
          if(index < stars){
            $(this).addClass('btn-warning');
          }
          else{
            $(this).addClass('btn-grey');
          }
        });

        // Updates average stars
        $('#average').html(response['average_evaluation']);

      }

    },
    error: function(data) {
      alert('ajax problem');
    }
  });
});
