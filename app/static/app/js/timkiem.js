$(document).ready(function() {
    $('#search-form input').change(function() {
        var $form = $('#search-form');
        $.ajax({
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(response) {
                $('#search-results').html(response.html);
            }
        });
    });
});
