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

table = $("#example").DataTable({
            dom: "<'table-scrollable't><'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",
            //dom :"Bfrtip",
            lengthChange: true,
            processing: true,
            serverSide: true,
            scrollY: "43vh",
            scrollCollapse: false,
            filter : false,
            displayLength: 25,
            stateSave : true,
            searching : false,
            "lengthMenu": [
                [30,50, 100, 150, 200,250,300,400,500,600,-1],
                [30,50, 100, 150, 200,250,300,400,500,600, "All"] // change per page values here
            ],
            "sPaginationType": "full_numbers",
            ajax: {
                url: "/datas/{{ model_name }}/{{ role_name }}/",
                type: "post"
            },
            columns: [
                {% for column in columns %}
                    {{ column.render | safe }}
                    {% if forloop.last %}{% else %},{% endif %}
                {% endfor %}
            ],
            select: true,
            buttons : true,
            language: {
                "lengthMenu": "Display _MENU_ records per page",
                "zeroRecords": "Nothing found - sorry",
                "info": "Showing page _PAGE_ of _PAGES_",
                "infoEmpty": "empty dddddddd",
                "infoFiltered": "filter dddddddd",
                buttons : {
                    pageLength: {
                        "_" : "%d条/页",
                        "-1" : "显示所有数据"
                    }
                }
            }
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
                    alert("filter")
                }
            },
        ]
    } );

    table.buttons().container().appendTo(
        $("#myaction")
    );