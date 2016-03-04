#-*- encoding:utf8 -*-
import re
from django.db import models as db_models
from django.db.models import Model,ForeignKey
from django.template import loader,Context
from util import loader as myloader
import json

from sms import base

class ModelMetaClass(type):
    def __new__(cls,name,bases,attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ModelMetaClass)]
        if parents:
            for obj_name, obj in attrs.items():
                Model.add_to_class(obj_name, obj)
        return super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)

class MetroModelBase(object):
    __metaclass__ = ModelMetaClass

class MetroModelAbstract(MetroModelBase):
    manageable = False
    #将一条记录序列化为id,text字典

    primary_key_name = u'id'
    xuexiao_field_name = u'xx'

    #根据角色过滤数据，不同角色需要改写该方法
    @classmethod
    def filter(cls,request):
        return cls.objects.all()

    @classmethod
    def ajax_tree_items(cls,request,role,field):
        return {
            u'id':'',
            u'text':u'%s对象还没有实现读取节点的方法。'%cls.path(),
            u'children':True
        }

    def item(self):
        return {u"id":getattr(self,self.primary_key_name),u"name":unicode(self)}

    @classmethod
    def items(cls,records):
        result = []
        for record in records:
            result.append(record.item())
        return result

    @classmethod
    def path(cls):
        return u"%s.%s"%(cls.__module__,cls.__name__)

    @classmethod
    def get_url(cls):
        url = u"/page/%s/"%cls.path()
        return url

    #获取模版
    @classmethod
    def get_template(cls):
        path = cls.path().replace(u".",u"/")
        path = path.lower()
        path += u'.html'
        try:
            return loader.get_template(path)
        except:
            return loader.get_template(u"page.html")

    #模型名和角色名
    @classmethod
    def model_name_and_role_name(cls,request):
        return request.path.split(u'/')[2:-1]

    #上下文
    @classmethod
    def get_context(cls,request):
        model_name,role_name = cls.model_name_and_role_name(request)
        return Context({
            u'request':request,
            u'search_fields' : cls.search_fields(request),
            u'columns' : cls.fields(request),
            u'edits' : cls.edit_fields(request),
            u'actions' : cls.actions_to_model(request),
            u'model_name' : model_name,
            u'role_name' : role_name
        })



    #显示列名
    field_names = []
    #编辑列名
    edit_field_names = []
    #可查找列名
    search_field_names = []
    #可进行操作的动作
    action_names = [u'create',u'edit',u'remove',u'copy',u'excel',u'pdf',u'print',u'search']

    #将显示列名转换为对应base.py中对应的对象
    @classmethod
    def fields(cls,request):
        _fields = cls._meta.fields + cls._meta.many_to_many
        _columns = []
        for item in cls.field_names:
            if isinstance(item,(str,unicode)):
                _columns.append(cls._meta.get_field_by_name(item)[0])
            elif isinstance(item,dict):
                _columns.append(item)

        _columns = _columns if _columns else _fields

        result = []
        for column in _columns:
            if isinstance(column,db_models.Field):
                if column.name == u'id':
                    continue
                result.append(getattr(base,u'Column%s'%column.__class__.__name__)(request,column))
            elif isinstance(column,dict):
                column_class = column.get(u'column_class')
                params = column.copy()
                del params[u'column_class']
                params[u'request'] = request
                result.append(column_class(**params))
        return result

    #将编辑列名转换为对应base.py中对应的对象
    @classmethod
    def edit_fields(cls,request):
        result = []

        for name in cls.edit_field_names:
            if name==u'id':
                continue
            if isinstance(name,dict):
                params = name.copy()
                if params.has_key(u'edit_class'):
                    edit_class = params.pop(u'edit_class')
                    result.append(edit_class(**params))
                elif params.has_key(u'field_name'):
                    field  = cls._meta.get_field_by_name(params.pop(u'field_name'))[0]
                    edit_class = getattr(base,u'Edit%s'%field.__class__.__name__)
                    params[u'request'] = request
                    params[u'field'] = field
                    result.append(edit_class(**params))
                pass
            elif isinstance(name,(unicode,str)):
                field = cls._meta.get_field_by_name(name)[0]
                edit_class = getattr(base,u"Edit%s"%field.__class__.__name__)
                result.append(edit_class(request,field))
            else:
                field = name
                edit_class = getattr(base,u'Edit%s'%field.__class__.__name__)
                result.append(edit_class(request,field))
        return result

    #将查找列名转换为对应base.py中对应的对象
    @classmethod
    def search_fields(cls,request):
        result = []
        for item in cls.search_field_names:
            if isinstance(item,dict):
                search_class = item.get(u'search_class')
                params = {key : value for key,value in item.items() if key!=u'search_class'}
                params[u'request'] = request
                params[u'main_model'] = cls
                result.append(search_class(**params))
            elif isinstance(item,(unicode,str)):
                field = cls._meta.get_field_by_name(item)[0]
                search_class = getattr(base,u'Search%s'%field.__class__.__name__)
                result.append(search_class(request,field))
            else:
                field = item
                search_class = getattr(base,u'Search%s'%field.__class__.__name__)
                result.append(search_class(request,field))

        return result

    ##将操作转换为对应base.py中对应的对象
    @classmethod
    def actions_to_model(cls,request):
        result = []
        for action in cls.action_names:
            result.append(base.ActionModel(request,cls,action,action.title()))

        return result

    #将一行数据转换为dict
    def row(self,request,fields):
        result = {}
        for field in fields:
            result[field.name] = field.data(self)
        result[u'id'] = getattr(self,self.primary_key_name)
        return result

    #将record转换为json格式时输出的列
    @classmethod
    def rows_fields(cls,request):
        result = {field.name:field for field in cls.fields(request)}
        for field in cls.edit_fields(request):
            result[field.name] = field
        return result

    #将一组记录转换为json对象
    @classmethod
    def rows(cls,request,records):
        data = []
        fields = cls.rows_fields(request).values()
        for record in records:
            data.append(record.row(request,fields))

        return {
            u'data':data
        }

    @classmethod
    def analysis_post(cls,request):
        result = {
            u'columns' : {},
            u'orders' : {},
            u'draw' : 0,
            u'length' : 0,
            u'start' : 0
        }

        def columns_data(key,value,match_obj):
            num = match_obj.groups()[0]
            result[u'columns'][num] = value

        def order_column(key,value,match_obj):
            num = match_obj.groups()[0]
            orders = result[u'orders'].get(num,{})
            orders[u'name'] = request.POST.get(u'columns[%s][data]'%value)
            result[u'orders'][num] = orders

        def order_dir(key,value,match_obj):
            num = match_obj.groups()[0]
            orders = result[u'orders'].get(num,{})
            orders[u'dir'] = value
            result[u'orders'][num] = orders

        def draw(key,value,match_obj):
            result[u'draw'] = value

        def length(key,value,match_obj):
            result[u'length']  = value

        def start(key,value,match_obj):
            result[u'start'] = value

        patterns = [
            (u'columns\[(\d+)\]\[data\]',columns_data),
            (u'order\[(\d+)\]\[column\]',order_column),
            (u'order\[(\d+)\]\[dir\]',order_dir),
            (u'draw',draw),
            (u'length',length),
            (u'start',start)
        ]
        for key,value in request.POST.items():
            for pattern,math in patterns:
                match_obj = re.match(pattern,key)
                if match_obj:
                    math(key,value,match_obj)

        return result

    #输出数据
    @classmethod
    def datas(cls,request):

        post_data = cls.analysis_post(request)

        records = cls.filter(request)
        total_count = records.count()

        for field in cls.search_fields(request):
            records = field.search(records)

        filter_count = records.count()


        length = int(post_data[u'length'])
        start = int(post_data[u'start'])
        if length<>-1:
            result = cls.rows(request,records[start:(start+length)])
        else :
            result = cls.rows(request,records)

        result[u'draw'] = post_data[u"draw"]
        result[u'recordsFiltered'] = filter_count
        result[u'recordsTotal'] = total_count
        return result

    #数据表操作接口，在视图中根据参数调用add,edit,delete执行具体操作
    @classmethod
    def do_action(cls,request):
        action = request.POST.get(u'action')
        return getattr(cls,u'do_action_%s'%action)(request)


    @classmethod
    def save_instance(cls,request,instance,ID):
        many_to_many_fields = []

        for field in cls.edit_fields(request):
            if issubclass(field.field.__class__,db_models.ManyToManyField):
                many_to_many_fields.append(field)
                continue
            field.setattr(instance,ID)

        instance.save1(request=request)
        for field in many_to_many_fields:
            field.setattr(instance,ID)
            instance.save()

    @classmethod
    def get_primary_keys(cls,request):
        result = []
        for k in request.POST.keys():
            try:
                result.append(re.search(u'data\[(\d+)\]\[id\]', k).groups()[0])
            except:
                pass
        if not result:
            return None
        elif len(result) == 1:
            return int(result[0])
        else:
            return result

    @classmethod
    def do_action_create(cls,request):
        obj = cls()
        cls.save_instance(request,obj,0)
        return cls.rows(request,[obj])


    @classmethod
    def do_action_edit(cls,request):
        def pk():
            for k in request.POST.keys():
                try:
                    return re.search(u'data\[(\d+)\]',k).groups()[0]
                except:
                    pass
            return None

        ID = pk()
        obj = cls.objects.get(pk=ID)
        cls.save_instance(request,obj,ID)
        return cls.rows(request,[obj])

    @classmethod
    def do_action_remove(cls,request):
        pks = cls.get_primary_keys(request)
        if pks is None:
            pks = []
        if isinstance(pks, int):
            pks = [pks]

        start = 0;
        targets = pks[start:start + 100]
        while targets:
            cls.objects.filter(pk__in=targets).delete()
            start += 100
            targets = pks[start:start + 100]
        return {u'data': []}


    def save1(self, force_insert=False, force_update=False, using=None,update_fields=None,request=None):
        model = self.__class__
        try:
            model._meta.get_field_by_name(self.xuexiao_field_name)
            try:
                xx_value = getattr(self,self.xuexiao_field_name)
            except:
                xx_value = None
            xx = request.user.xx
            if xx_value is None and xx is not None:
                setattr(self,self.xuexiao_field_name,xx)
        except:
            pass
        self.save(force_insert=force_insert,force_update=force_update,using=using,update_fields=update_fields)
        pass


class MetroModel(MetroModelAbstract):
    pass