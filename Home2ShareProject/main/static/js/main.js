$('.rating-block button').hover(function(event){
  $('.rating-block button').removeClass('btn-warning btn-grey');
  $(this).addClass('btn-warning');
  $(this).prevAll().addClass('btn-warning');
  $(this).nextAll().addClass('btn-grey');
});

$('.rating-block button').on('click', function(event){
  event.preventDefault();
  var frm = $('#form_eval');
  var button = $(this);
  var stars = button.attr('data-value');
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
