function logoutUser(button) {
    let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    $.ajax({
        type: "POST",
        url: button.dataset.url,
        headers:{"X-CSRFToken": csrf_token},
        success: function () {
            window.location.replace(button.dataset.success);
        }
    });
}