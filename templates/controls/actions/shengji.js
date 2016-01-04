{
    text:'{{ title }}',
    action : function(e, dt, node, config) {
        bootbox.confirm('确定进行升级操作？',function(result){
            if(result){
                $.ajax({
                    url : '/action/{{model.path}}/{{role_name}}/',
                    type : 'post',
                    data : {
                        'action' : '{{ extend }}'
                    }
                })
            }
        })
    }
}