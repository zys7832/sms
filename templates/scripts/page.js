var table,editor;
editor = new $.fn.dataTable.Editor({
            ajax: "/action/{{ model_name }}/{{ role_name }}/",
            table: "#example",
            idSrc: "id",
            fields: [
                {% for edit in edits %}
                    {% if forloop.last %}
                        {{ edit.render | safe }}
                    {% else %}
                        {{ edit.render | safe }},
                    {% endif %}
                {% endfor %}
            ]
});

var validater = $(editor.dom.form).validate({
            rules : {
                    {% for edit in edits %}
                        {% if forloop.last %}
                            '{{ edit.rule_name }}':{{ edit.validate_rules | safe }}
                        {% else %}
                            '{{ edit.rule_name }}':{{ edit.validate_rules | safe }},
                        {% endif %}
                    {% endfor %}
                }
            }),
            edit_fields = [
                    {% for edit in edits %}
                    {% if not edit.editable %}
                        {% if forloop.last %}
                            '{{ edit.name }}'
                        {% else %}
                            '{{ edit.name }}',
                        {% endif %}
                    {% endif %}
                {% endfor %}
            ]

        editor.on( 'open', function( e, mode, action ) {
            for (var index in edit_fields){
                editor.field(edit_fields[index]).rules(action)
            }
            validater.resetForm()
        } );


        editor.on( 'preSubmit', function ( e, o, action ){
            if(action!=='remove'){
                return $(editor.dom.form).valid()
            }
        })

table = $("#example").DataTable({
            dom: "<'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",
            //dom :"Bfrtip",
            lengthChange: true,
            processing: true,
            serverSide: true,
            scrollY: "43vh",
            scrollCollapse: false,
            filter : false,
            displayLength: 50,
            stateSave : true,
            searching : false,
            "lengthMenu": [
                [50, 100, 150, 200,250,300,400,500,600,-1],
                [50, 100, 150, 200,250,300,400,500,600, "All"] // change per page values here
            ],
            "sPaginationType": "full_numbers",
            ajax: {
                url: "/datas/{{ model_name }}/{{ role_name }}/",
                type: "post",
                data:function(d){
                    var arr = $("#search_form").serializeArray()
                    for (index in arr) {
                        d[arr[index].name] = arr[index].value
                    }
                }
            },
            columns: [
                {% for column in columns %}
                    {{ column.render | safe }}
                    {% if forloop.last %}{% else %},{% endif %}
                {% endfor %}
            ],
            'aaSorting':[
                {% for column in columns %}
                    {% if column.ordering %}
                        [{{ forloop.counter0 }},'{{ column.direction }}']
                        {% if forloop.last %}{% else %},{% endif %}
                    {% endif %}
                {% endfor %}
                ],
            select: true,
            buttons : true
});


new $.fn.dataTable.Buttons( table, {
        buttons: [
            {
                extend: 'collection',
                text: '输出 <i class="fa fa-angle-down"></i>',
                buttons: [
                    'copy',
                    'pdf',
                    'excel',
                    'print'
                ]
            },
            {
                extend: 'collection',
                text: '操作 <i class="fa fa-angle-down"></i>',
                buttons: [
                    {
                        'text' : 'New',
                        'extend' : 'create',
                        'editor' : editor
                    },
                    {
                        'text' : 'Edit',
                        'extend' : 'edit',
                        'editor' : editor
                    },
                    {
                        'text' : 'Delete',
                        'extend' : 'remove',
                        'editor' : editor
                    }
                ]
            },
            {
                'text' : '显示/隐藏列 <i class="fa fa-angle-down"></i>',
                'extend' : 'colvis'
            },
            'pageLength',
            {
                'text' : '过滤 <i class="fa fa-filter"></i>',
                'action' : function(){
                    $("#filter").modal()
                }
            },
        ]
    } );

    table.buttons().container().appendTo(
        $("#myaction")
    );

$("#post_search").click(function(event){
    $("#filter").modal("hide")
    table.ajax.reload()
})