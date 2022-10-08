
function loadCanvas() {
    var data = $(".visibility-on").toArray().map(item => item.parentElement.dataset.id)
    
    $.ajax({
        method: "GET",
        url: $("[name=data-plot]").data("url"),
        dataType: 'json',
            data: {
                'array': JSON.stringify(data)
            },
        success: function (response) {
            $("#canvas").html(response.canvas)
        }
    });
}

function enableOptions() {
    $(".visibility-on").click(function (e) {
        if($(this).hasClass("visibility-on")){
            $(this).removeClass("visibility-on");
            $(this).addClass("visibility-off");
            $(this).html("visibility_off");
            loadCanvas()
        }else{
            $(this).removeClass("visibility-off");
            $(this).addClass("visibility-on");
            $(this).html("visibility");
            loadCanvas()
        }
    });

    $(".pencil").click(function (e) {
        var formData = $(this).parent().data('id')
        $.ajax({
            method: "GET",
            url: $("[name=data-table]").data("url"),
            dataType: 'json',
            data: {
                'id': formData
            },
            success: function (response) {
                let data = response[0][0]
                $("#id-plot").data("id", data.id)
                $("#measure-date-edit").val(data.measure_date.substring(0,16))
                $("#module-type-edit").val(data.module_type)
                $("#reference-edit").val(data.reference)
                $("#temperature-edit").val(data.temperature)
                $("#modalEdit").modal('show')
            }
        });
    });

    $(".delete").click(function (e) {
        Swal.fire({
            title: '¿Estás seguro(a)?',
            text: "Esta operación es irreversible",
            icon: 'warning',
            showCancelButton: true,
            cancelButtonColor: '#3085d6',
            confirmButtonColor: '#d33',
            confirmButtonText: 'Borrar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                'Borrado!',
                'La medición ha sido borrada.',
                'success'
                )
                var formData = $(this).parent().data('id')
                $.ajax({
                    method: "DELETE",
                    url: $("[name=data-table]").data("url"),
                    dataType: 'json',
                    headers:{"X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()},
                    data: {
                        'id': formData
                    },
                    success: function (response) {
                        window.location.reload()
                    }
                });
            }
        })
    });
    loadCanvas()
}

function getTableData(){
    data = $("[name=min_temperature], [name=max_temperature], [name=min_date], [name=max_date]").serialize()
    Swal.fire({
        title: 'Cargando tabla',
        timer: 500,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading()
            $.ajax({
                method: "GET",
                url: $("[name=data-table]").data("url"),
                data: data,
                success: function (response) {
                    $("#table-body").html("")
                    var str = ``
                    response[0].forEach(element => {
                        let datetime = new Date(element.measure_date)
                        datetime = datetime.toDateString()
                        str = str + `
                        <tr>
                            <td data-id=${element.id}>
                                <button class="material-icons visibility-on">visibility</button>
                                <button class="material-icons visibility-off" hidden>visibility_off</button>
                                <button class="material-icons pencil">mode_edit</button>
                                <button class="material-icons delete">delete</button>
                            </td>
                            <td>${datetime}</td>
                            <td>${element.module_type}</td>
                            <td>${element.reference}</td>
                            <td>${element.temperature}</td>
                        </tr>`
                    })
                    $("#table-body").html(str)
                    enableOptions()
                }
            });
        }
    })
}



$( document ).ready(function() {
    getTableData();
    enableOptions();

    $(".file-input").change(function (e) { 
        if($(this).val())
            $(".btn-import").attr("disabled", false)
        else
            $(".btn-import").attr("disabled", true)
    });

    $(".btn-filter").click(function (e) {
        getTableData()
    });

    $(".btn-import").click(function (e) {
        var data = new FormData();
        data.append("file", $(".file-input")[0].files[0])
        data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val())
        $.ajax({
            method: "POST",
            url: $(this).data("url"),
            processData: false,
            contentType: false,
            mimeType: "multipart/form-data",
            data: data,
            success: function (response) {
            getTableData();
            enableOptions();
        }
        });
    });
    $(".btn-edit-measure").click(function (e) { 
        $.ajax({
            method: "PUT",
            url: $("[name=data-table]").data("url"),
            headers:{"X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()},
            data: {
                id: $("#id-plot").data("id"),
                measure_date: $("#measure-date-edit").val(),
                module_type: $("#module-type-edit").val(),
                reference: $("#reference-edit").val(),
                temperature: $("#temperature-edit").val()
            },
            success: function (response) {
                getTableData();
                enableOptions();
            }
        });
    });
    
});