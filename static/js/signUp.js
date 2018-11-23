$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                window.document.innerHTML = response
            },
            error: function(error) {
                window.document.innerHTML = response
            }
        });
    });
});
