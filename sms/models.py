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



class MetroModel(MetroModelBase):
    manageable = False
    #将一条记录序列化为id,text字典

    primary_key_name = u'id'

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

    @classmethod
    def get_context(cls,request):
        model_name,role_name = request.path.split(u'/')[2:-1]
        return Context({
            u'request':request,
            u'search_fields' : cls.search_fields(request),
            u'columns' : cls.fields(request),
            u'edits' : cls.edit_fields(request),
            u'model_name' : model_name,
            u'role_name' : role_name
        })

    field_names = []
    edit_field_names = []
    search_field_names = []

    @classmethod
    def fields(cls,request):
        _fields = cls._meta.fields + cls._meta.many_to_many
        _fields = [cls._meta.get_field_by_name(name)[0] for name in cls.field_names] if cls.field_names else _fields
        result = []
        for field in _fields:
            if field.name==u'id':
                continue
            result.append(getattr(base,u'Column%s'%field.__class__.__name__)(request,field))
        return result

    @classmethod
    def edit_fields(cls,request):
        result = []

        for name in cls.edit_field_names:
            if name==u'id':
                continue
            if isinstance(name,dict):
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

    def row(self,request,fields):
        result = {}
        for field in fields:
            result[field.name] = field.data(self)
        result[u'id'] = getattr(self,self.primary_key_name)
        return result

    @classmethod
    def rows_fields(cls,request):
        result = {field.name:field for field in cls.fields(request)}
        for field in cls.edit_fields(request):
            result[field.name] = field
        return result

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
    def datas(cls,request):
        records = cls.objects.all()

        for field in cls.search_fields(request):
            records = field.search(records)

        number_of_page = int(request.POST.get(u'numberOfPage',70))
        current_page = int(request.POST.get(u'currentPage',1))
        count = records.count()
        if number_of_page==-1:
            number_of_page = 1 if count==0 else count
            current_page = 1

        result = cls.rows(request,records[(current_page-1)*number_of_page:current_page*number_of_page])

        result[u'currentPage'] = current_page
        total_pages,r = divmod(count,number_of_page)
        if r>0:
            total_pages += 1

        result[u'totalPages'] = total_pages
        result[u'numberOfPage'] = number_of_page
        result[u'records'] = count
        return result

    #数据表操作接口，在视图中根据参数调用add,edit,delete执行具体操作
    @classmethod
    def do_action(cls,request):
        def pk():
            for k in request.POST.keys():
                try:
                    return re.search(u'data\[(\d+)\]',k).groups()[0]
                except:
                    pass
            return None

        obj = cls()
        action = request.POST.get(u'action')
        if action==u'remove':
            pass
            return {u'data':[]}
        if action==u'edit':
            ID = pk()
            obj = cls.objects.get(pk=ID)
        else:
            ID = 0

        many_to_many_fields = []

        for field in cls.edit_fields(request):
            if issubclass(field.field.__class__,db_models.ManyToManyField):
                many_to_many_fields.append(field)
                continue
            field.setattr(obj,ID)

        obj.save()
        for field in many_to_many_fields:
            field.setattr(obj,ID)
            obj.save()

        return cls.rows(request,[obj])
