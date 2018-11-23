$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                document.body.parentElement.innerHTML  = response;
            },
            error: function(error) {
                document.body.parentElement.innerHTML  = response;
            }
        });
    });
});
