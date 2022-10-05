function loginUser(button) {
    $.ajax({
        type: "POST",
        url: button.dataset.url,
        data: {
            "email": $("#email").val(),
            "password": $("#password").val(),
        },
        dataType: "json",
        success: function () {
            window.location = button.dataset.success
        }
    });
}