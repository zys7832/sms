#-*- encoding:utf8 -*-
import json
import base64
import smtplib
from email.mime.text import MIMEText

from django import http
from django.db import models as db_models
from django.shortcuts import render
from accounts import models as accounts_models
from django.contrib import auth
from django.contrib.auth.models import User,make_password
from django.template.loader import Context
from util import loader


def index(request):
    return render(request,"index.html")

def login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if user:
            if not user.is_active:
                result = {u"code":1,u"text":u"用户被冻结无法登陆！"}
            else:
                auth.login(request,user)
                result = {u"code":0,u"text":request.GET.get(u"next_url","/")}
        else:
            result = {u'code':1,u'text':u"用户名称或密码不正确！"}

        return http.HttpResponse(json.dumps(result),content_type=u"application/json")
    schools = accounts_models.Xuexiao.objects.all()
    return render(request,"login.html",{"schools":schools})

def send_mail(request):
    email = request.POST.get("email")
    try:
        user = User.objects.get(email=email)
    except:
        return http.HttpResponse(u"请输入注册时使用的邮箱地址！")
    pk = make_password(u"%s_%s"%(user.username,email),None,"pbkdf2_sha256")
    user.reset_password = pk;
    user.save()
    url = u"%s/rpass/?pk1=%s&pk2=%s"%(request.environ["HTTP_HOST"],base64.b64encode(pk),base64.b64encode(email))
    t = u"""
    <html>
        <body>
            <h3>重置用户密码</h3>
            <p>尊敬的用户您好!<br>
            您使用""" + email +u"""邮箱在本站注册了一个用户，您现在请求重置密码。如果不是本人操作，请忽略之，多有打扰清凉解。<br>如果是本人操作，请将链接复制到浏览器地址栏中"""+url+u"""
            </p>
        </body>
    </html>
    """

    sender = u'zys7832@163.com'
    receiver = email
    subject = u'重置用户密码'
    username = u'zys7832@163.com'
    password = u'78325042@163.com'

    msg = MIMEText(t,'html','utf-8')

    msg['Subject'] = subject

    smtp = smtplib.SMTP()
    smtp.connect(u'smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    response_json = {u"code":1,u"text":u"请登陆邮%s箱继续操作"%email}
    return http.HttpResponse(json.dumps(response_json),content_type=u"application/json")

def get_grade(request,school_id):
    grades = accounts_models.Nianji.objects.filter(xx__id=school_id).order_by("order")
    result = accounts_models.Nianji.items(grades)
    return http.HttpResponse(json.dumps(result),content_type=u"application/json")

def get_klass(request,grade_id):
    klasses = accounts_models.Banji.objects.filter(nj_id=grade_id).order_by("order")
    result = accounts_models.Banji.items(klasses)
    return http.HttpResponse(json.dumps(result),content_type=u"application/json")

def validator(request,path,field):
    model = loader.load_model(path)
    value = request.REQUEST.get(field)
    q = db_models.Q()
    q.children.append((field,value))
    count = model.objects.filter(q).count()
    #return http.HttpResponse(u"true")
    return http.HttpResponse(u"true" if count==0 else u"false")

def register_user(request):
    if request.POST:
        realname = request.POST.get("first_name","")
        username = request.POST.get("username","")
        email = request.POST.get("email","")
        school = request.POST.get("school",None)
        klass = request.POST.get("klass",None)
        password = request.POST.get("password","")
        rpassword = request.POST.get("rpassword","")
        sfzjh = request.POST.get("sfzjh","")
        if password=="":
            return http.HttpResponse({"code":1,"text":u"密码不能为空！"},content_type="application/json")
        elif password!=rpassword:
            return http.HttpResponse({"code":1,"text":u"两次输入的密码不一致！"},content_type="application/json")
        user = User()
        user.username = username
        user.email = email
        user.first_name = realname
        user.school = accounts_models.Xuexiao.objects.get(id=school)
        user.password = make_password(password)
        user.sfzjh = sfzjh
        if klass:
            user.bj = accounts_models.Banji.objects.get(id=klass)
        try:
            user.save()
            return http.HttpResponse(json.dumps({"code":1,u"text":u"用户创建成功！"}),content_type="application/json")
        except Exception,e:
            return http.HttpResponse(json.dumps({"code":1,"text":u"班村数据失败！"}),content_type="application/json")
    else:
        return http.HttpResponse(json.dumps({"code":1,"text":u"不知道啥意思？"}),content_type="application/json")

def reset_password(request):
    if request.POST:
        password = request.POST.get("password","")
        rpassword = request.POST.get("rpassword","")
        email = request.POST.get("email","")
        if password==rpassword:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.reset_password=""
                user.save(update_fields=["reset_password"])
                return http.HttpResponse(json.dumps({"code":1,u"text":u"修改密码成功，请牢记。"}),content_type="application/json")
            except:
                return http.HttpResponse(json.dumps({"code":1,u"text":u"该用户不存在，无法修改。"}),content_type="application/json")

    pk = base64.b64decode(request.GET.get("pk1",""))
    email = request.GET.get("pk2","")

    if not (pk and email):
        raise http.Http404(u"你访问的页面不存在")
    email = base64.b64decode(email)
    try:
        user = User.objects.get(email=email,reset_password=pk)
    except:
        raise http.Http404(u"你访问的页面不存在")

    return render(request,u"reset_password.html",{u"email":email})

def page(request,path,role=None):
    model = loader.load_member(request,path,role)
    t = model.get_template()
    return http.HttpResponse(t.render(model.get_context(request)))

def datas(request,path,role):
    model = loader.load_member(request,path,role)
    records = model.datas(request)
    return http.HttpResponse(json.dumps(records),content_type=u"application/json")


def action(request,path,role):
    model = loader.load_member(request,path,role)
    result = model.do_action(request)
    return http.HttpResponse(json.dumps(result),content_type=u"application/json")

def items(request,path,role):
    model = loader.load_member(request,path,role)
    parent_model_path = request.GET.get(u'parent_model',None)
    parent_id = request.GET.get(u'parent_id')
    child_model_name = path.rsplit(u'.')[-1].lower()
    all_records = model.objects.all()
    records = all_records
    if parent_model_path and parent_id:
        try:
            parent_model = loader.load_member(request,parent_model_path,role)
            parent = parent_model.objects.get(pk=parent_id)
            manager = getattr(parent,u'%s_set'%child_model_name)
            records = manager.all()
            if all_records.count()<records.count():
                records = all_records
        except Exception as e:
            records = []
    records = model.items(records)
    return http.HttpResponse(json.dumps(records),content_type=u"application/json")

def ajax_tree_items(request,path,role,field):
    model = loader.load_member(request,path,role)
    result = model.ajax_tree_items(request,role,field)
    return http.HttpResponse(json.dumps(result),content_type=u"application/json")