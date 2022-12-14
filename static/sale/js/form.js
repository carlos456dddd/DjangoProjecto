var tblProducts;


var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.0,
        total: 0.00,
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva=0.18;
        
        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cant * parseFloat(dict.precio);
            subtotal+=dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();

       tblProducts= $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "nombre.nombre"},
                {"data": "categoria.nombrecategoria"},
                {"data": "precio"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
    


            
            initComplete: function (settings, json) {

            }
        });
    },
};
function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}
function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, 
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

$(function () {

    
    function alertaction(title, content, callback) {
        $.confirm({
            theme: 'material',
            title: title,
            icon: 'fa fa-info',
            content: content,
            columnClass: 'small',
            typeAnimated: true,
            cancelButtonClass: 'btn-primary',
            draggable: true,
            dragWindowBorder: false,
            buttons: {
                info: {
                    text: "Si",
                    btnClass: 'btn-primary',
                    action: function () {
                      callback();
                    }
                },
                danger: {
                    text: "No",
                    btnClass: 'btn-red',
                    action: function () {
    
                    }
                },
            }
        })
    }
    $('.datepicker').datepicker({
        ok: '',
        clear: 'Clear selection',
        close: 'Cancel'
      })
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('input[name="date_joined"]').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
       
    });


    // buscar productos

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
               
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal=0.0;
           
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });

    
    $('.btnRemoveAll').on('click',function(){
        if(vents.items.products.length==0)return false;
        alertaction('Notificación','¿Seguro de eliminar todos?',function(){
            vents.items.products=[];
            vents.list();
        });
    
    });

    $('#tblProducts tbody').on('click','a[rel="remove"]',function(){
        var tr=tblProducts.cell($(this).closest('td,li')).index();
        alertaction('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?', function () {
            vents.items.products.splice(tr.row, 1);
            vents.list();
        });
      
    })
    
    .on('change keyup','input[name="cant"]',function()
   
    { 
        var cant=parseInt($(this).val());
        var tr=tblProducts.cell($(this).closest('td,li')).index();
        vents.items.products[tr.row].cant=cant;
       vents.calculate_invoice();
       $('td:eq(5)',tblProducts.row(tr.row).node()).html('$'+vents.items.products[tr.row].subtotal.toFixed(2));
    }
    );
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(vents.items.products.length === 0){
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }
        
    
       vents.items.date_joined=$('input[name="date_joined"]').val();
       vents.items.cli=$('input[name="cli"]').val();
        var parameters=new FormData()

        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/usuario/vendedor/';
        });
    });

});