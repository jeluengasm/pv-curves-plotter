function registerUser() {
    let data = $('#formReg').serialize();
    $.ajax({
        type: 'POST',
        url: $("#formReg").data('url'),
        data: data,
        dataType: 'json',
        encode: true,
    }).done(function (data) {
        window.location = button.dataset.success
    });
}