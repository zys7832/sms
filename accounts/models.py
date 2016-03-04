#-*- encoding:utf8 -*-

from django import http
from django.db import models as db_models
from django.template import loader,Context
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.utils import timezone
from common import models as com_models
from collections import OrderedDict
from sms import base as sms_base,fields as sms_fields
import json

class Xuexiao(db_models.Model):
    xxmc = db_models.CharField(max_length=255,verbose_name=u"学校名称")
    xxdz = db_models.CharField(max_length=255,verbose_name=u"学校地址")
    xzxm = db_models.CharField(max_length=50,verbose_name=u"校长姓名")
    jxny = db_models.DateField(verbose_name=u"建校年月")
    lxdh = db_models.CharField(max_length=30,blank=True,verbose_name=u"联系电话")
    czdh = db_models.CharField(max_length=30,blank=True,verbose_name=u"传真电话")
    dzyx = db_models.EmailField(blank=True,verbose_name=u"电子邮箱")
    zydz = db_models.URLField(blank=True,verbose_name=u"主页地址")
    xxbbm = db_models.ForeignKey(com_models.xxbb,null=True,blank=True,verbose_name=u"学校办别")
    szdmzsx = db_models.BooleanField(verbose_name=u"少数民族学校")
    xxxz = db_models.IntegerField(verbose_name=u"小学学制",default=0)
    xxrxnl = db_models.IntegerField(verbose_name=u"小学入学年龄",default=6)
    czxz = db_models.IntegerField(verbose_name=u"初中学制",default=0)
    czrxnl = db_models.IntegerField(verbose_name=u"初中入学年龄",default=0)
    gzxz = db_models.IntegerField(verbose_name=u"高中学制",default=3)

    def __unicode__(self):
        return self.xxmc

    class Meta:
        verbose_name = u'学校'
        ordering = [u'xxmc',u'-xxdz']

    edit_field_names = [u'xxmc',u'xxdz',u'xzxm',u'jxny',u'lxdh',u'dzyx',u'xxbbm',u'szdmzsx']

class Nianji(db_models.Model):
    njmc = db_models.CharField(max_length=30,verbose_name=u"年级名称")
    order = db_models.IntegerField(default=0,verbose_name=u'年级序号')
    xx = db_models.ForeignKey(Xuexiao,verbose_name=u'学校')

    def __unicode__(self):
        return self.njmc

    @property
    def prev(self):
        try:
            return Nianji.objects.get(xx=self.xx,order=self.order-1)
        except:
            return None

    @property
    def next(self):
        try:
            return Nianji.objects.get(xx=self.xx,order=self.order+1)
        except:
            return None

    class Meta:
        verbose_name = u"年级"

    def get_xuexiao(self):
        return self.xx

    @classmethod
    def do_action_shengji(cls,request):
        user = request.user
        user.xx.nianji_set.get(order=4).banji_set.update(nj=None)
        user.xx.nianji_set.get(order=3).banji_set.update(nj=user.xx.nianji_set.get(order=4))
        user.xx.nianji_set.get(order=2).banji_set.update(nj=user.xx.nianji_set.get(order=3))
        user.xx.nianji_set.get(order=1).banji_set.update(nj=user.xx.nianji_set.get(order=2))
        return {}

    field_names = [u'njmc',u'order']
    edit_field_names = [u'njmc',u'order']


class Banji(db_models.Model):
    bh = db_models.CharField(max_length=15,blank=True,verbose_name=u"班级号")
    bj = db_models.CharField(max_length=255,verbose_name=u"班级名称")
    jbny = db_models.DateField(verbose_name=u"建班日期")
    bzrgh = sms_fields.MyAjaxTreeForeignKey(u'Jiaozhigong',blank=True,null=True,verbose_name=u"班主任",related_name=u'bzrgh_to_account') #db_models.ForeignKey
    bzxh = sms_fields.MyAjaxTreeForeignKey(u'Xuesheng',null=True,blank=True,verbose_name=u"班长",related_name='bzxh_to_account')
    bjrych = db_models.TextField(verbose_name=u"班级荣誉称号",blank=True)
    xz = db_models.IntegerField(verbose_name=u"学制",default=4)
    bjlxm = db_models.ForeignKey(com_models.zxxbjlx,null=True,blank=True,verbose_name=u"班级类型")
    byrq = db_models.DateField(verbose_name=u"毕业日期")
    sfssmzsyjxb = db_models.BooleanField(verbose_name=u"少数民族双语教学班",default=False)
    syjxmsm = db_models.ForeignKey(com_models.ssmzsyjxms,blank=True,null=True,verbose_name=u"双语教学模式")
    nj = db_models.ForeignKey(Nianji,blank=True,null=True,verbose_name=u"所属年级")
    order = db_models.IntegerField(default=0,verbose_name=u'班级序号')

    edit_field_names = [u'bh',u'bj',u'jbny',u'bzrgh',u'bzxh',u'nj']
    search_field_names = [u'nj']
    class Meta:
        verbose_name = u"班级"

    def __unicode__(self):
        return self.bj

    @classmethod
    def get_banji_by_user(cls,user):
        try:
            return Banji.objects.filter(bzrgh__pk=user.pk).order_by("-jbny")[0]
        except:
            return None

    def get_nianji(self):
        try:
            return self.nj
        except:
            return None

    def get_xuexiao(self):
        try:
            return self.nj.get_xuexiao()
        except:
            return None

class Object(db_models.Model):
    text = db_models.CharField(max_length=100,verbose_name=u'管理对象名')
    path = db_models.CharField(max_length=100,verbose_name=u'完整路径')

    edit_field_names = [u'text',u'path']

    def __unicode__(self):
        return u'%s'%self.text

class NavigatorManager(db_models.Manager):
    def objects(self):
        return self.filter(model__isnull=False,summary__isnull=False)

    def roots(self):
        return self.filter(parent__isnull=True)

    def children(self,parent_id):
        return self.filter(parent__parent_id=parent_id)

class Navigator(db_models.Model):
    j_id = db_models.CharField(max_length=50,verbose_name=u'节点ID')
    text = db_models.CharField(max_length=100,verbose_name=u'节点显示文本')
    parent = sms_fields.TreeForeignKey(u"self",verbose_name=u'父节点',blank=True,null=True)
    icon = db_models.CharField(max_length=30,blank=True,null=True)

    objects = NavigatorManager()
    primary_key_name = u'j_id'

    def __unicode__(self):
        return u'%s'%self.text

    def menu_item(self):
        child = OrderedDict()
        parent = self
        while parent:
            result = OrderedDict({
                u'id' : self.j_id,
                u'text' : self.text,
                u'icon' : self.icon,
                u"children" : child
            })
            child = result
            parent = parent.parent

        return result

    def node(self):
        result = OrderedDict({})
        result[u'id'] = self.j_id
        result[u'text'] = self.text
        result[u'icon'] = self.icon

        for child in self.__class__.objects.filter(parent=self):
            if not result.has_key(u'children'):
                result[u'children'] = []
            result[u'children'].append(child.node())
        return result

    @classmethod
    def nodes(cls):
        result = []
        for root in cls.objects.roots():
            result.append(root.node())
        return result

    @classmethod
    def get_template(cls):
        return loader.get_template(u'accounts/models/position.html')

    @classmethod
    def get_context(cls,request):
        model_name,role_name = request.path.split(u'/')[2:-1]
        return Context({
            u'request':request,
            u'model_name' : model_name,
            u'role_name' : role_name,
            u'items' : json.dumps(cls.nodes())
        })

    @classmethod
    def do_action(cls,request):
        action = request.POST.get(u'action')
        if action==u'add':
            obj = cls(text=request.POST.get(u'text'),parent=cls.objects.get(j_id=request.POST.get(u'pid')),j_id=request.POST.get(u'j_id'))
            obj.save()
        elif action==u'rename':
            obj = cls.objects.get(j_id=request.POST.get(u'j_id'))
            obj.text = request.POST.get(u'text')
            obj.save()
        elif action==u'delete':
            cls.objects.filter(j_id=request.POST.get(u'j_id')).delete();
        elif action==u'move':
            j_id = request.POST.get(u'j_id')
            pid = request.POST.get(u'pid')
            obj = cls.objects.get(j_id=j_id)
            obj.parent = cls.objects.get(j_id=pid)
            obj.save()
        elif action==u'icon':
            j_id = request.POST.get(u'j_id')
            icon = request.POST.get(u'icon')
            obj = cls.objects.get(j_id=j_id)
            obj.icon = icon
            obj.save()
            pass
        return {u'result':u'ok'}


    edit_field_names = [u'text',u'icon',u'parent']

class Action(db_models.Model):
    text = db_models.CharField(max_length=100,verbose_name=u'操作名称')
    url = db_models.CharField(max_length=255,verbose_name=u'操作URL')
    identity = db_models.CharField(max_length=50,verbose_name=u'操作标示',unique=True)
    icon = db_models.CharField(max_length=30,blank=True,null=True)

    edit_field_names = [u'text',u'url',u'identity',u'icon']

    def __unicode__(self):
        return u'%s'%self.text

class GroupAction(db_models.Model):# 更名为GroupPostionAction
    group = db_models.ForeignKey(Group,verbose_name=u'执行该操作的角色')
    navigator = sms_fields.TreeForeignKey(Navigator,verbose_name=u'在导航中的位置')
    action = db_models.ForeignKey(Action,verbose_name=u'执行的操作')
    object = db_models.ForeignKey(Object,verbose_name=u'操作对象')
    layout = db_models.CharField(max_length=100,verbose_name=u'页面布局文件',null=True,blank=True)


    edit_field_names = [u'group',u'navigator',u'action',u'object',u'layout']
    search_field_names = [u'group',u'navigator',u'action',u'object']

    class Meta:
        unique_together = ((u'group',u'object',u'action'),)
        ordering = [u'group__id',u'object__id',u'action__id']

    @classmethod
    def searchforeignkey_navigator(cls,request,records):
        value = request.POST.get(u'navigator',None)
        if value:
            try:
                records = records.filter(navigator__j_id=u'%s'%value)
            except:
                pass
        return records

class GroupBaseMetaClass(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, GroupBaseMetaClass)]
        if parents:
            #fields = []
            for obj_name, obj in attrs.items():
                #if isinstance(obj, db_models.Field): fields.append(obj_name)
                Group.add_to_class(obj_name, obj)

            #GroupAdmin.fieldsets = list(GroupAdmin.fieldsets)
            #GroupAdmin.fieldsets.append((name, {'fields': fields}))
        return super(GroupBaseMetaClass, cls).__new__(cls, name, bases, attrs)

class GroupBase(object):
    __metaclass__ = GroupBaseMetaClass

class MyGroup(GroupBase):
    summary = db_models.CharField(max_length=50,verbose_name=u"介绍")

    def actions(self):
        return GroupAction.objects.filter(group__id=self.id).order_by("object__id")

    def actions_by_object(self,object_name):
        return [record.action for record in self.actions().filter(object__model=object_name)]

    def menus(self):
        result = OrderedDict()
        object_ids = [item[u'object'] for item in self.actions().values(u'object').distinct()]
        objects = Object.objects.filter(id__in=object_ids)
        for obj in objects:
            child = obj.menu_item()
            current = result
            while child:
                if not current.has_key(child.id):
                    current[id] = child
                current = current[id][u'children']
                child = child.get(u'children')

        return result

    def __unicode__(self):
        return self.summary

class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, db_models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class Profile(object):
    __metaclass__ = ProfileBase

class MyProfile(Profile):
    sfzjh = sms_fields.MySfzjhCharField(max_length=30,verbose_name=u"身份证号码",unique=True)
    xbm = db_models.ForeignKey(com_models.xb,verbose_name=u"性别",blank=True,null=True)
    mzm = db_models.ForeignKey(com_models.gbmz,verbose_name=u"民族",blank=True,null=True)
    jkzkm = db_models.ForeignKey(com_models.gbjkzk,verbose_name=u"健康状况",blank=True,null=True)
    csrq = db_models.DateField(verbose_name=u"出生日期",blank=True,null=True)
    sjhm = db_models.CharField(max_length=100,verbose_name=u"手机号",blank=True)
    txdz = db_models.CharField(max_length=255,blank=True,verbose_name=u"通信地址")
    yzbm = db_models.CharField(max_length=6,blank=True,verbose_name=u"邮政编码")
    jtzz = db_models.CharField(max_length=255,blank=True,verbose_name=u"家庭住址")
    xzz = db_models.CharField(max_length=255,blank=True,verbose_name=u"现住址")
    hkszd = db_models.CharField(max_length=255,blank=True,verbose_name=u"户口所在地")
    rxny = db_models.DateField(verbose_name=u"入学年月",default=timezone.now(),blank=True,null=True)
    bj = db_models.ForeignKey(Banji,blank=True,null=True,verbose_name=u'班级')
    xx = db_models.ForeignKey(Xuexiao,verbose_name=u'学校',blank=True,null=True)
    reset_password = db_models.CharField(blank=True,null=True,max_length=300)

    REQUIRED_FIELDS = [u"email",u"sfzjh"]

    @classmethod
    def ajax_tree_items(cls,request,role,field):
        records = cls.filter(request)
        parent = request.POST.get(u'parent',u'#')
        result = []
        if parent==u'#':
            exsiteds = []
            for record in records:
                try:
                    xing = record.first_name[0]
                except:
                    continue
                if exsiteds.count(xing)==0:
                    exsiteds.append(xing)
                    result.append({
                        u'id' : xing,
                        u'text' : xing,
                        u'children':True
                    })
        else:
            records = records.filter(first_name__startswith=parent)
            for record in records:
                result.append({
                    u'id' : record.id,
                    u'text' : record.first_name
                })

        return result

    def __unicode__(self):
        return u'%s'%self.first_name



class Account(User):
    class Meta:
        proxy = User

    @classmethod
    def filter(cls,request):
        if request.user.xx:
            records = cls.objects.filter(xx=request.user.xx)
        else:
            records = cls.objects.all()
        return records

class Xuesheng(User):
    class Meta:
        proxy = User

    @classmethod
    def filter(cls,request):
        return cls.objects.filter(xx=request.user,bj__isnull=False)

    def get_nianji(self):
        return self.bj.nj

class Jiaozhigong(User):
    class Meta:
        proxy = User

    @classmethod
    def filter(cls,request):
        return cls.objects.filter(xx=request.user.xx,bj__isnull=True)


class Config(User):
    class Meta:
        proxy = True

    @classmethod
    def filter(cls,request):
        if request.user.xx:
            records = cls.objects.filter(xx=request.user.xx)
        else:
            records = cls.objects.all()
        return records

    field_names = [u'id',u'first_name',u'username',u'email',u'sfzjh',u'is_superuser',u'is_active',u'is_staff',u'date_joined',u'last_login',u'groups',u'xx']
    edit_field_names = [u'first_name',
                        u'username',
                        {
                            u'field_name':u'email',
                            u'editable' : False,
                            u'unique' : True
                        },
                        u'sfzjh',
                        u'is_superuser',u'is_active',u'is_staff',u'date_joined',u'last_login',u'groups',u'xx']
    search_field_names = [u'first_name',u'username',u'email',u'sfzjh',u'is_superuser',u'is_active',u'is_staff',
        {
            u'search_class' : sms_base.SearchForeignKey3,
            u'model1' : Xuexiao,
            u'model2' : Nianji,
            u'model3' : Banji,
            u'field_name1' : u'xx',
            u'field_name2' : u'nj',
            u'field_name3' : u'bj'
        }]


    @classmethod
    def searchforeignkey_nj(cls,request,records):
        nianji = request.POST.get(u'nj',None)
        if nianji:
            return records.filter(bj__nj__pk=nianji)
        else:
            return records


class MyGroup(Group):
    class Meta:
        proxy = True

    field_names = [u'id',u'name',u'summary']
    edit_field_names = [u'id',u'name',u'summary']
    search_field_names = [u'name']