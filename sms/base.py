#-*- encoding:utf8 -*-

from django.db import models as dmodels
from django.template import loader ,Context
from util.loader import load_member
import json

class BaseField(object):
    def __init__(self,request,field):
        self.request = request
        self.field = field
        self.direction = u''
    @property
    def name(self):
        return self.field.name

    @property
    def verbose_name(self):
        return u'%s'%self.field.verbose_name

    def data(self,obj):
        return getattr(obj,self.name)

    def ordering(self):
        if self.name in self.field.model._meta.ordering:
            self.direction = u'asc'
            return True
        elif u'-%s'%self.name in self.field.model._meta.ordering:
            self.direction = u'desc'
            return True
        return False

class ColumnGeneratorField(object):
    def __init__(self,request,name,verbose_name):
        self.request = request
        self.__name = name
        self.__verbose_name = verbose_name

    @property
    def name(self):
        return self.__name

    @property
    def verbose_name(self):
        return self.__verbose_name

    def data(self,obj):
        return getattr(obj,self.name)

    def render(self):
        return json.dumps({u"data":self.name})

class ColumnField(BaseField):
    def render(self):
        return json.dumps({u"data":self.name})


class ColumnBooleanField(ColumnField):
    def get_template(self):
        return loader.get_template(u'controls/columns/booleanfield_column.html')

    def get_context(self):
        return Context({
            u'field':self
        })

    def render(self):
        return self.get_template().render(self.get_context())

class ColumnCharField(ColumnField):
    pass

class ColumnMyCharField(ColumnCharField):
    pass

class ColumnMySfzjhCharField(ColumnCharField):
    pass

class ColumnDateField(ColumnField):
    def data(self,obj):
        return unicode(getattr(obj,self.name))


class ColumnDateTimeField(ColumnDateField):
    pass

class ColumnDecimalField(ColumnField):
    pass

class ColumnMyDecimalField(ColumnDecimalField):
    pass

class ColumnEmailField(ColumnCharField):
    pass

class ColumnFilePathField(ColumnField):
    pass

class ColumnFloatField(ColumnField):
    pass

class ColumnMyFloatField(ColumnFloatField):
    pass

class ColumnIntegerField(ColumnField):
    pass

class ColumnMyIntegerField(ColumnIntegerField):
    pass

class ColumnBigIntegerField(ColumnIntegerField):
    pass

class ColumnIPAddressField(ColumnField):
    pass

class ColumnGenericIPAddressField(ColumnField):
    pass

class ColumnNullBooleanField(ColumnField):
    pass

class ColumnPositiveIntegerField(ColumnIntegerField):
    pass

class ColumnPositiveSmallIntegerField(ColumnIntegerField):
    pass

class ColumnSlugField(ColumnCharField):
    pass

class ColumnSmallIntegerField(ColumnIntegerField):
    pass

class ColumnTextField(ColumnField):
    pass

class ColumnTimeField(ColumnField):
    pass

class ColumnURLField(ColumnCharField):
    pass

class ColumnForeignKey(ColumnField):
    def render(self):
        return json.dumps({u"data" : u"%s.name"%self.name})

    def data(self,obj):
        try:
            value = getattr(obj,self.name)
            return value.item()
        except:
            return {u'id':u'',u'name':u''}

class ColumnTreeForeignKey(ColumnForeignKey):
    pass

class ColumnMyAjaxTreeForeignKey(ColumnTreeForeignKey):
    pass

class ColumnManyToManyField(ColumnField):
    def render(self):
        result =  {
            u'data' : self.name,
            u'render' : u'[,].name'
        }
        return json.dumps(result)

    def data(self,obj):
        value = getattr(obj,self.name)
        records = value.all()
        result = []
        for record in records:
            result.append(record.item())

        return result



class SearchField(object):
    def __init__(self,request,field):
        self.request = request
        self.field = field
        self.role_name = self.request.path.split(u'/')[-2]

    @property
    def template(self):
        name = u'controls/search/%s_search.html'%self.field.__class__.__name__.lower()
        return loader.get_template(name)

    @property
    def context(self):
        return Context({
            u'request' : self.request,
            u'field' : self.field
        })

    def render(self):
        return self.template.render(self.context)

    @property
    def name(self):
        return self.field.name

    @property
    def verbose_name(self):
        return u'%s'%self.field.verbose_name

    def search(self,records):
        return records
    
class SearchBooleanField(SearchField):
    def search(self,records):
        value = self.request.POST.get(self.field.name,None)
        if value==u'true':
            value = True
        elif value==u'false':
            value = False
        else:
            value = None

        if value is None:
            return records
        q = dmodels.Q()
        q.children.append((self.field.name,value))
        return records.filter(q)


class SearchCharField(SearchField):
    def search(self,records):
        value = self.request.POST.get(self.field.name,None)
        if not value:
            return records
        q = dmodels.Q()
        q.children.append((self.field.name+'__icontains',value))
        return records.filter(q)


class SearchMyCharField(SearchCharField):
    pass

class SearchMySfzjhCharField(SearchMyCharField):
    pass

class SearchDateField(SearchField):
    pass

class SearchDateTimeField(SearchField):
    pass

class SearchDecimalField(SearchField):
    pass

class SearchMyDecimalField(SearchDecimalField):
    pass

class SearchEmailField(SearchCharField):
    pass

class SearchFilePathField(SearchField):
    pass

class SearchFloatField(SearchField):
    pass

class SearchMyFloatField(SearchFloatField):
    pass

class SearchIntegerField(SearchField):
    pass

class SearchMyIntegerField(SearchIntegerField):
    pass

class SearchBigIntegerField(SearchIntegerField):
    pass

class SearchIPAddressField(SearchField):
    pass

class SearchGenericIPAddressField(SearchField):
    pass

class SearchNullBooleanField(SearchField):
    pass

class SearchPositiveIntegerField(SearchIntegerField):
    pass

class SearchPositiveSmallIntegerField(SearchIntegerField):
    pass

class SearchSlugField(SearchCharField):
    pass

class SearchSmallIntegerField(SearchIntegerField):
    pass

class SearchTextField(SearchField):
    pass

class SearchTimeField(SearchField):
    pass

class SearchURLField(SearchCharField):
    pass

class SearchForeignKey(SearchField):
    @property
    def context(self):
        main_model_by_role = load_member(self.request,self.field.rel.to.path(),self.role_name)
        records = main_model_by_role.objects.all()
        records = main_model_by_role.items(records)
        return Context({
            u'request' : self.request,
            u'field' : self.field,
            u'options' : records
        })

    def search(self,records):
        value = self.request.POST.get(self.field.name)
        if value:
            try:
                method = getattr(self.field.model,u'searchforeignkey_%s'%self.field.name)
                records = method(self.request,records)
            except:
                q = dmodels.Q()
                q.children.append((u'%s__pk'%self.field.name,value))
                records = records.filter(q)

        return records

class SearchTreeForeignKey(SearchForeignKey):
    @property
    def context(self):
        #return super(SearchTreeForeignKey,self).context
        return Context({
            u'request' : self.request,
            u'field' : self.field,
            u'items' : json.dumps(self.field.rel.to.nodes())
        })

class SearchMyAjaxTreeForeignKey(SearchTreeForeignKey):
    @property
    def context(self):
        model_path = self.field.rel.to.path() if self.field.get_tree_item_from_field_to else self.field.model.path()
        return Context({
            u'request' : self.request,
            u'field' : self.field,
            u'ajax_url' : u'/ajax_tree_items/%s/%s/%s/'%(model_path,self.role_name,self.name)
        })


class SearchForeignKey2(SearchField):
    def __init__(self,request,main_model,model1,model2,field_name1,field_name2):
        self.request = request
        self.role_name = self.request.path.split(u'/')[-2]
        self.main_model = main_model
        self.model1 = model1
        self.model2 = model2
        self.field_name1 = field_name1
        self.field_name2 = field_name2

    @property
    def name(self):
        return u'searchforeignkey2'

    @property
    def context(self):
        main_model_by_role = load_member(self.request,self.model1.path(),self.role_name)
        records = main_model_by_role.objects.all()
        records = main_model_by_role.items(records)
        return Context({
            u'request' : self.request,
            u'main_model' : self.main_model,
            u'model1' : self.model1,
            u'model2' : self.model2,
            u'field_name1' : self.field_name1,
            u'field_name2' : self.field_name2,
            u'field_verbose_name1' : self.model1._meta.verbose_name,
            u'field_verbose_name2' : self.model2._meta.verbose_name,
            u'options' : records,
            u'role_name' : self.role_name
        })

    def search(self,records):
        value1 = self.request.POST.get(self.field_name1,None)
        value2 = self.request.POST.get(self.field_name2,None)
        if value1:
            try:
                method = getattr(self.main_model,u'searchforeignkey_%s'%self.field_name1)
                records = method(self.request,records)
            except:
                field = self.main_model._meta.get_field_by_name(self.field_name1)[0]
                if (field):
                    q = dmodels.Q()
                    q.children.append((u'%s__pk'%field.name,value1))
                    records = records.filter(q)
        if value2:
            try:
                method = getattr(self.main_model,u'searchforeignkey_%s'%self.field_name2)
                records = method(self.request,records)
            except:
                try:
                    field = self.main_model._meta.get_field_by_name(self.field_name2)[0]
                except:
                    field = None

                if (field):
                    q = dmodels.Q()
                    q.children.append((u'%s__pk'%field.name,value1))
                    records = records.filter(q)
        return records

    @property
    def template(self):
        name = u'controls/search/searchforeign2_search.html'
        return loader.get_template(name)

class SearchForeignKey3(SearchForeignKey2):
    def __init__(self,request,main_model,model1,model2,model3,field_name1,field_name2,field_name3):
        super(SearchForeignKey3,self).__init__(request,main_model,model1,model2,field_name1,field_name2)
        self.model3 = model3
        self.field_name3 = field_name3

    @property
    def context(self):
        result = super(SearchForeignKey3,self).context
        result[u'model3'] = self.model3
        result[u'field_name3'] = self.field_name3
        result[u'field_verbose_name3'] = u'%s'%self.model3._meta.verbose_name
        return result

    @property
    def template(self):
        name = u'controls/search/searchforeign3_search.html'
        return loader.get_template(name)


    def search(self,records):
        records = super(SearchForeignKey3,self).search(records)
        value3 = self.request.POST.get(self.field_name3,None)
        if value3:
            try:
                method = getattr(self.main_model,u'searchforeignkey_%s'%self.field_name1)
                records = method(self.request,records)
            except:
                try:
                    field = self.main_model._meta.get_field_by_name(self.field_name3)[0]
                    if (field):
                        q = dmodels.Q()
                        q.children.append((u'%s__pk'%field.name,value3))
                        records = records.filter(q)
                except:
                    pass

        return records


class EditField(BaseField):
    def __init__(self,request,field,editable=True,unique=False,**kwargs):
        super(EditField,self).__init__(request,field)
        self.role_name = request.path.split(u'/')[-2]
        self.editable = not self.field.unique if editable else False #editable
        self.kwargs = kwargs
        self.__unique = True if unique else field.unique

    def render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = self.name
        result[u'type'] = u'mtext'
        result[u'editable'] = self.editable
        result[u'rules'] = self.rules()
        return json.dumps(result)

    def key(self,pk):
        return u'data[%s][%s]'%(pk,self.field.name)


    def value(self,pk):
        return self.field.to_python(self.request.POST.get(self.key(pk)))

    def setattr(self,obj,pk):
        setattr(obj,self.name,self.value(pk))

    def required(self):
        return not (self.field.null and self.field.blank)

    def unique(self):
        result = {u'type':u'get'}
        result[u'url'] = u'/validator/%s/%s/'%(self.field.model.path(),self.name)
        result[u'cache'] = False
        result[u'async'] = False
        return result

    def rules(self):
        result = {}
        if self.required():
            result[u'required'] = True
        if self.__unique:
            result[u'remote']  = self.unique()
        return result

    @property
    def rule_name(self):
        return self.name

    def validate_rules(self):
        return json.dumps(self.rules())

class EditBooleanField(EditField):
    def render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = self.field.name
        result[u'type'] = u'mradio'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable
        result[u'options'] = [
            {u'label':u'是',u'value':True},
            {u'label':u'否',u'value':False}
        ]
        return json.dumps(result)


    def value(self,pk):
        v = self.request.POST.get(self.key(pk))
        if v in (u'true',u'false'):
            v = v.title()
        return self.field.to_python(v)


class EditCharField(EditField):
    def max_length(self):
        return self.field.max_length

    def rules(self):
        result = super(EditCharField,self).rules()
        result[u'maxlength']  = self.max_length()
        return result

    def required(self):
        return not self.field.blank

class EditMyCharField(EditCharField):
    def equalto(self):
        return self.field.to_field

    def min_length(self):
        return self.field.min_length

    def rules(self):
        result = super(EditMyCharField,self).rules()
        if self.field.min_length:
            result[u'minlength'] = self.min_length()
        if self.field.to_field:
            result[u'equalTo'] = u'#%s'%self.name
        return result

class EditMySfzjhCharField(EditCharField):
    def rules(self):
        result = super(EditMySfzjhCharField,self).rules()
        result[u'isidcardno'] = True
        return result

class EditDateField(EditField):
    def build_render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = self.field.name
        result[u'type'] = u'mdate'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable

        return result

    def render(self):
        return json.dumps(self.build_render())

    def data(self,obj):
        return unicode(getattr(obj,self.name))

    def date(self):
        return True

    def rules(self):
        result = super(EditDateField,self).rules()
        result[u'date'] = self.date()
        return result

class EditDateTimeField(EditDateField):
    def build_render(self):
        result = super(EditDateTimeField,self).build_render()
        result[u'type'] = u'mdatetime'
        return result

    def rules(self):
        result = super(EditDateTimeField,self).rules()
        try:
            result.pop(u"date")
        except:
            pass
        result[u'datetime'] = True
        return result

class EditDecimalField(EditField):
    def number(self):
        return True

    def rules(self):
        result = super(EditDecimalField,self).rules()
        result[u'number'] = self.number()
        return result

class EditMyDecimalField(EditDecimalField):
    def max(self):
        return self.field.max

    def min(self):
        return self.field.min

    def rules(self):
        result = super(EditMyDecimalField)
        if self.field.max:
            result[u'max'] = self.max()
        if self.field.min:
            result[u'min'] = self.min()
        return result

class EditEmailField(EditCharField):
    def email(self):
        return True;

    def rules(self):
        result = super(EditEmailField,self).rules()
        result[u'email'] = self.email()
        return result

class EditFilePathField(EditField):
    pass

class EditFloatField(EditField):
    def number(self):
        return True

    def rules(self):
        result = super(EditFloatField,self).rules()
        result[u'number'] = self.number()
        return result

class EditMyFloatField(EditFloatField):
    def max(self):
        return self.field.max

    def min(self):
        return self.field.min

    def rules(self):
        result = super(EditMyFloatField,self).rules()
        if self.field.max:
            result[u'max'] = self.max()
        if self.field.min:
            result[u'min'] = self.min()

        return result


class EditIntegerField(EditField):
    def digits(self):
        return True

    def rules(self):
        result = super(EditIntegerField,self).rules()
        result[u'digits'] = self.digits()
        return result

class EditMyIntegerField(EditIntegerField):
    def max(self):
        return self.field.max

    def min(self):
        return self.field.min

    def rules(self):
        result = super(EditMyIntegerField,self).rules()
        if self.field.max:
            result[u'max'] = self.max()
        if self.field.min:
            result[u'min'] = self.min()
        return result

class EditBigIntegerField(EditIntegerField):
    pass

class EditIPAddressField(EditField):
    pass

class EditGenericIPAddressField(EditField):
    pass

class EditNullBooleanField(EditField):
    pass

class EditPositiveIntegerField(EditIntegerField):
    pass

class EditPositiveSmallIntegerField(EditIntegerField):
    pass

class EditSlugField(EditCharField):
    pass

class EditSmallIntegerField(EditIntegerField):
    pass

class EditTextField(EditField):
    pass

class EditTimeField(EditField):
    pass

class EditURLField(EditCharField):
    def url(self):
        return True

    def rules(self):
        result = super(EditURLField,self).rules()
        result[u'url'] = self.url()
        return result

class EditForeignKey(EditField):
    def render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = u'%s.id'%self.field.name
        result[u'type'] = u'mselect'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable
        result[u'options'] = []
        model = load_member(self.request,self.field.rel.to.path(),self.role_name)
        for record in model.objects.all():
            result[u'options'].append({u'label':unicode(record),u'value':record.id})

        return json.dumps(result)

    @property
    def rule_name(self):
        return u'%s.id'%self.name


    def key(self,pk):
        return u'data[%s][%s][id]'%(pk,self.field.name)


    def value(self,pk):
        v = self.request.POST.get(self.key(pk))
        try:
            q = dmodels.Q()
            q.children.append((self.field.rel.to.primary_key_name,v))
            return self.field.rel.to.objects.get(q)
        except:
            return None

    def data(self,obj):
        try:
            value = getattr(obj,self.name)
        except:
            value = None
        if value:
            return value.item()
        else:
            return {u'id':u'',u'name':u''}

class EditTreeForeignKey(EditForeignKey):
    def render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = u'%s.id'%self.field.name
        result[u'type'] = u'treeselect1'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable
        model = load_member(self.request,self.field.rel.to.path(),self.role_name)
        result[u'items'] = model.nodes()

        return json.dumps(result)

class EditMyAjaxTreeForeignKey(EditForeignKey):
    def render(self):
        model_path = self.field.rel.to.path() if self.field.get_tree_item_from_field_to else self.field.model.path()
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = u'%s.id'%self.field.name
        result[u'type'] = u'ajaxtreeselect'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable
        result[u'ajax_url'] = u'/ajax_tree_items/%s/%s/%s/'%(model_path,self.role_name,self.name)
        return json.dumps(result)


class EditManyToManyField(EditField):
    def render(self):
        result = {}
        result[u'label'] = u'%s'%self.field.verbose_name
        result[u'name'] = u'%s[].id'%self.field.name
        result[u'type'] = u'mmselect'
        result[u'rules'] = self.rules()
        result[u'editable'] = self.editable
        result[u'options'] = []
        model = load_member(self.request,self.field.rel.to.path(),self.role_name)
        for record in model.objects.all():
            result[u'options'].append({u'label':unicode(record),u'value':record.id})
        return json.dumps(result)

    def many_to_many_count(self,pk):
        return int(self.request.POST.get(u'data[%s][%s-many-count]'%(pk,self.name)))


    def value(self,pk):
        result = []
        for index in range(self.many_to_many_count(pk)):
            ID = self.request.POST.get(u'data[%s][%s][%s][id]'%(pk,self.field.name,index))
            result.append(self.field.rel.to.objects.get(pk=ID))
        return result

    def data(self,obj):
        value = getattr(obj,self.name)
        records = value.all()
        result = []
        for record in records:
            result.append(record.item())

        return result


########################################################################################################################
# Action相关类
########################################################################################################################

class ActionModel(object):
    def __init__(self,request,model,action_name,title):
        self.request = request
        self.model = model
        self.action_name = action_name
        self.title = title
        self.role_name = request.path.split(u'/')[-2]

    def get_template(self):
        template_path = u'controls/actions/%s/%s/%s.js'%(self.role_name,self.model.__module__,u'%s_%s'%(self.model.__name__.lower(),self.action_name))
        try:
            return loader.get_template(template_path)
        except:
            try:
                return loader.get_template(u'controls/actions/%s.js'%self.action_name)
            except:
                return loader.get_template(u'controls/actions/action.js')

    def context(self):
        return Context({
            u'request':self.request,
            u'model' : self.model,
            u'role_name' : self.role_name,
            u'title' : self.title,
            u'extend' : self.action_name
        })

    def render(self):
        return self.get_template().render(self.context())