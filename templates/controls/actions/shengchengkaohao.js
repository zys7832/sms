{
    text:'{{ title }}',
    action : function(e, dt, node, config) {
        bootbox.confirm('确定需要生成考号，该操作会覆盖之前的操作？',function(result){
            var row_id = $("#example").DataTable().row({selected:true}).data().id
            if(result){
                Metronic.blockUI({
                    boxed: true
                });
                $.ajax({
                    url : '/action/{{model.path}}/{{role_name}}/?kaoshi_id='+row_id,
                    type : 'post',
                    data : {
                        'action' : '{{ extend }}'
                    },
                    success : function(response){
                        bootbox.alert(response.info)
                        Metronic.unblockUI();
                    }
                })
            }
        })
    },
    className : 'daorukaosheng',
    enabled : false
}