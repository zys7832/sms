#-*- encoding:utf8 -*-
from miniui import fields,controls,utils

class GatqwForeignKeyControl(fields.ForeignKeyControl):
    control = controls.AutoComplete    
    def __init__(self,**kwargs):
        super(GatqwForeignKeyControl,self).__init__(**kwargs)
        
    @classmethod
    def control_datas(cls,request,model):      
        objects = []  
        model = utils.get_member(model)
        filter_= utils.get_master_factory_class(model).filter
        records = filter_(request.user,model)
        key = request.POST.get("key",None)
        if key is not None:
            records = records.filter(name__icontains=key)
        for record in records:
            objects.append({model.id_field:getattr(record,model.id_field),model.text_field:getattr(record,model.text_field)})
        return objects
