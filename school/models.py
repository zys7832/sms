#-*- encoding:utf8 -*-
import datetime

from django.db import models as db_models,connection
from common import models as common_models
from accounts import models as accounts_models
from sms import fields as sms_fields

from school import sqls


class Kecheng(db_models.Model):
    kch = db_models.CharField(max_length=10,verbose_name=u"课程号")
    kcmc = db_models.CharField(max_length=20,verbose_name=u"课程名称")
    kcm = db_models.ForeignKey(common_models.zxxkc,verbose_name=u"课程码",blank=True,null=True)
    kcdjm = db_models.ForeignKey(common_models.zxxkcdj,verbose_name=u"中小学课程等级",blank=True,null=True)
    kcbm = db_models.CharField(max_length=60,blank=True,verbose_name=u"课程别名")
    kcjj = db_models.CharField(max_length=300,blank=True,verbose_name=u"课程简介")
    kcyq = db_models.CharField(max_length=300,blank=True,verbose_name=u"课程要求")
    zxs = db_models.IntegerField(verbose_name=u"总学时")
    zhxs = db_models.IntegerField(verbose_name=u"周学时")
    zxxs = db_models.IntegerField(verbose_name=u"自学学时",default=0)
    skfsm = db_models.ForeignKey(common_models.skfs,null=True,blank=True,verbose_name=u"授课方式")
    cksm = db_models.CharField(max_length=300,blank=True,verbose_name=u"参考书目")
    zongfen = db_models.IntegerField(verbose_name=u'总分',default=100)
    yxfs = db_models.IntegerField(verbose_name=u'优秀分数',default=80)
    jgfs = db_models.IntegerField(verbose_name=u'及格分数',default=60)
    csfs = db_models.IntegerField(verbose_name=u'差生分数',default=30)

    def __unicode__(self):
        return self.kcmc

    class Meta:
        verbose_name = u'课程管理'

    edit_field_names = [u'kch',u'kcmc',u'kcm',u'kcdjm',u'kcbm',u'kcjj',u'kcyq',u'zxs',u'zhxs',u'zxxs',u'skfsm',u'zongfen',u'yxfs',u'jgfs',u'csfs']
    search_field_names = [u'kcmc',u'kcdjm',u'skfsm']

class Xiaoli(db_models.Model):
    start = db_models.DateField(verbose_name=u'学期开是时间')
    end = db_models.DateField(verbose_name=u'学期结束时间')
    work_days = db_models.IntegerField(verbose_name=u'工作天数',default=0)
    holiday_days = db_models.IntegerField(verbose_name=u'放假天数',default=0)
    name = db_models.CharField(verbose_name=u'学期名称',max_length=30)
    current_term = db_models.BooleanField(u'当前学期')
    xx = db_models.ForeignKey(accounts_models.Xuexiao,verbose_name=u'学校')

    edit_field_names = [u'start',u'end',u'work_days',u'holiday_days',u'name',u'current_term']

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None,request=None):
        if self.current_term:
            self.__class__.objects.filter(current_term=True).update(current_term=False)
        super(Xiaoli,self).save(force_insert=force_insert,force_update=force_update,using=using,update_fields=update_fields)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = [u'-current_term',u'start']
        verbose_name = u'校历'

class Rili(db_models.Model):
    day = db_models.DateField(verbose_name=u'日期')
    work = db_models.BooleanField(verbose_name=u'是否上班')
    daiban1 = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'带班领导',blank=True,null=True,related_name=u'daiban1_to_account')
    daiban2 = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'中层1',blank=True,null=True,related_name=u'daiban2_to_account')
    daiban3 = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'中层2',blank=True,null=True,related_name=u'daiban3_to_account')
    zhiri = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'值日教师',blank=True,null=True,related_name=u'zhiri_to_account')
    zhixulingdao = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'值宿领导',blank=True,null=True,related_name=u'zhixulingdao_to_account')
    zhixujiaoshi = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'值宿教师',blank=True,null=True,related_name=u'zhixujiaoshi_to_account')
    fuzebumen = db_models.CharField(verbose_name=u'负责部门',max_length=20)
    gongzuoneirong = db_models.CharField(max_length=200,verbose_name=u'工作内容')
    xx = db_models.ForeignKey(accounts_models.Xuexiao,null=True,blank=True)

    field_names = [u'day',u'work',u'daiban1',u'daiban2',u'daiban3',u'zhiri',u'zhixulingdao',u'zhixujiaoshi',u'fuzebumen',u'gongzuoneirong']
    edit_field_names = [u'day',u'work',u'daiban1',u'daiban2',u'daiban3',u'zhiri',u'zhixulingdao',u'zhixujiaoshi',u'fuzebumen',u'gongzuoneirong']
    search_field_names = [u'day',u'work',u'daiban1',u'daiban2',u'daiban3',u'zhiri',u'zhixulingdao',u'zhixujiaoshi',u'fuzebumen',u'gongzuoneirong']
    class Meta:
        verbose_name = u'学校日历'

# 教学计划
class Jiaoxuejihua(db_models.Model):
    kch = db_models.ForeignKey(Kecheng,verbose_name=u"课程号")
    sknj = db_models.ForeignKey(accounts_models.Nianji,verbose_name=u"授课年级")
    skxqm = db_models.ForeignKey(Xiaoli,verbose_name=u"授课学期")
    ksfsm = db_models.ForeignKey(common_models.ksfs,verbose_name=u"考试方式")
    xx = db_models.ForeignKey(accounts_models.Xuexiao)

    edit_field_names = [u'kch',u'sknj',u'skxqm',u'ksfsm']
    class Meta:
        verbose_name = u'教学计划'

    def __unicode__(self):
        return u"%s-%s-%s"%(self.skxqm,self.sknj,self.kch)

# 教师分工表
class Jiaoshifengong(db_models.Model):
    xq = db_models.ForeignKey(Xiaoli,verbose_name=u"授课学期")
    kc = db_models.ForeignKey(Jiaoxuejihua,verbose_name=u'课程')
    bj = db_models.ForeignKey(accounts_models.Banji,verbose_name=u'班级')
    js = sms_fields.MyAjaxTreeForeignKey(accounts_models.Account,verbose_name=u'授课教师')

    class Meta:
        verbose_name=u'教师分工'
        ordering = [u'-xq__current_term',u'xq__start']

    edit_field_names = [u'xq',u'kc',u'bj',u'js']
    search_field_names = [u'xq',u'kc',u'bj',u'js']

# 排课数据
class Paike(db_models.Model):
    kch = db_models.ForeignKey(Jiaoxuejihua,verbose_name=u"课程")
    skbj = db_models.ForeignKey(accounts_models.Banji,verbose_name=u"授课班级")
    skrq = db_models.IntegerField(verbose_name=u"授课日期")
    skjs = db_models.IntegerField(verbose_name=u"节次")
    skxqm = db_models.ForeignKey(Xiaoli,verbose_name=u'授课学期')
    xx = db_models.ForeignKey(accounts_models.Xuexiao)

    edit_field_names = [u'kch',u'skbj',u'skrq',u'skjs']

    class Meta:
        verbose_name = u'排课'
        ordering = [u'skbj__order',u'skrq',u'skjs']

    def __unicode__(self):
        return u"%s-%s-%s"%(self.skjsgh,self.skbj,self.kch)

#教室信息
class Jiaoshi(db_models.Model):
    name = db_models.CharField(max_length=50,verbose_name=u'教室名称')
    xx = db_models.ForeignKey(accounts_models.Xuexiao)

    edit_field_names = [u'name']

    def __unicode__(self):
        return self.name

# 考试信息数据类
class Kaoshi(db_models.Model):
    ksmc = db_models.CharField(max_length=100,verbose_name=u"考试名称")
    ksnj = db_models.ForeignKey(accounts_models.Nianji,verbose_name=u'考试年级')
    ksxqm = db_models.ForeignKey(Xiaoli,verbose_name=u'学期')
    khcl = db_models.IntegerField(verbose_name=u'考号生成策略',default=0)
    kskssj = db_models.DateField(verbose_name=u'考试时间',default=datetime.datetime.now())
    sycks = db_models.ForeignKey("self",null=True,blank=True,verbose_name=u"上次考试")
    over = db_models.BooleanField(default=False,verbose_name=u'考试结束')
    kskm = db_models.ManyToManyField(Jiaoxuejihua,verbose_name=u'考试科目',blank=True,null=True)
    step = db_models.IntegerField(default=0)
    xx = db_models.ForeignKey(accounts_models.Xuexiao)

    edit_field_names = [u'ksmc',u'ksnj',u'ksxqm',u'khcl',u'kskssj',u'sycks',u'kskm']
    field_names = [u'ksmc',u'ksnj',u'ksxqm',u'khcl',u'kskssj',u'sycks']

    action_names = [u'create',u'edit',u'remove',u'daorukaosheng',u'shengchengkaohao',u'zhiliangfenxi']

    class Meta:
        verbose_name = u'考试管理'
        ordering = [u'-ksxqm__current_term',u'kskssj']

    def __unicode__(self):
        return u'%s-%s-%s'%(self.ksxqm,self.ksnj,self.ksmc)

    @classmethod
    def do_action_daorukaosheng(cls,request):
        kaoshi_id = int(request.GET.get("kaoshi_id"))
        Kaosheng.objects.filter(kaoshi__pk=kaoshi_id).delete()
        kaoshi = cls.objects.get(pk=kaoshi_id)

        excute_sql = u''
        if kaoshi.khcl==0 or kaoshi.sycks is None:
            excute_sql = sqls.daorukaosheng_from_xuesheng(kaoshi)
        elif kaoshi.khcl==1 and kaoshi.sycks:
            excute_sql = sqls.daorukaosheng_from_shangyicikaoshi(kaoshi)
        else:
            excute_sql = sqls.daorukaosheng_from_xuesheng(kaoshi)

        cursor = connection.cursor()
        cursor.execute(excute_sql)
        return {}

    @classmethod
    def do_action_shengchengkaohao(cls,request):

        return {}

    @classmethod
    def do_action_zhiliangfenxi(cls,request):

        return {}

class Kaoshikemu(db_models.Model):
    kaoshi = db_models.ForeignKey(Kaoshi,verbose_name=u'考试')
    kemu = db_models.ForeignKey(Jiaoxuejihua,verbose_name=u'考试科目')

    class Meta:
        verbose_name = u'考试科目'

    edit_field_names = [u'kaoshi',u'kemu']
    search_field_names = [u'kaoshi']

    def __unicode__(self):
        return self.kemu

class Kaoshikaochang(db_models.Model):
    kaoshi = db_models.ForeignKey(Kaoshi,verbose_name=u'考试')
    kaochangxuhao = db_models.IntegerField(verbose_name=u'考场序号')
    kaoshengshu = db_models.IntegerField(verbose_name=u'考生人数')
    jiaoshi = db_models.ForeignKey(Jiaoshi,verbose_name=u'教室')

    edit_field_names = [u'kaoshi',u'kaochangxuhao',u'kaoshengshu',u'jiaoshi']
    search_field_names = [u'kaoshi']
    class Meta:
        verbose_name = u'考试用考场'
        ordering = [u'-kaoshi__ksxqm__current_term']

    def __unicode__(self):
        return u'%s(%s)'%(self.kaochangxuhao,self.jiaoshi)

class Kaosheng(db_models.Model):
    kaoshi = db_models.ForeignKey(Kaoshi,verbose_name=u'考试')
    kaosheng = sms_fields.MyAjaxTreeForeignKey(accounts_models.Xuesheng,verbose_name=u'考生')
    kaochang = db_models.ForeignKey(Kaoshikaochang,verbose_name=u'考场')
    kaohao = db_models.IntegerField(verbose_name=u'考号',default=0)

    edit_field_names = [u'kaoshi',u'kaosheng',u'kaochang',u'kaohao']
    search_field_names = [u'kaoshi',u'kaosheng',u'kaochang',u'kaohao']

    class Meta:
        verbose_name = u'考生管理'
        ordering = [u'kaochang__kaochangxuhao',u'kaohao']

class Chengji(db_models.Model):
    kaoshi = db_models.ForeignKey(Kaoshi,verbose_name=u'考试')
    kaosheng = sms_fields.MyAjaxTreeForeignKey(accounts_models.Xuesheng,verbose_name=u'考生')
    kemu = db_models.ForeignKey(Kaoshikemu,verbose_name=u'考试科目')
    chengji = db_models.FloatField(verbose_name=u'考试成绩')



