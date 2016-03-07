{
    text:'{{ title }}',
    action : function(e, dt, node, config) {
        var row_id = -1
        try {
            row_id = $("#example").DataTable().row({selected: true}).data().id
        } catch (err){
            bootbox.alert('清选择一次考试！')
            return
        }
        bootbox.confirm('确定导入考生，该操作会覆盖之前的操作？',function(result){
            if(result){
                $.ajax({
                    url : '/action/{{model.path}}/{{role_name}}/?kaoshi_id='+row_id,
                    type : 'post',
                    data : {
                        'action' : '{{ extend }}'
                    }
                })
            }
        })
    },
    className : 'daorukaosheng',
    enabled : false
}