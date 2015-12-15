#-*- encoding:utf8 -*-
from django.contrib.auth.models import User
from django.utils.importlib import import_module
import json
from util.pinyin import Pinyin

def load_module(request,path,role):
    old_path = path
    module_path = path.split(u".",1)
    app = module_path[0]
    klass = module_path[-1]
    user = request.user
    if user.id is None:
        return None

    if user.is_superuser:
        return import_module(old_path)

    try:
        user.groups.get(name=role)
    except:
        return None

    path = []

    #app.roles.suihuadishizhongxue.role.username.[models].Class
    #app.roles.suihuadishizhongxue.role.[models].Class
    #app.roles.[models].Class
    #app.[models].Class

    if user.xx:
        path.append(u"%s.roles.schools.%s.%s.%s.%s"%(app,Pinyin.get_pinyin(user.xx.xxmc,u""),role.lower(),user.username.lower(),klass))
        path.append(u"%s.roles.schools.%s.%s.%s"%(app,Pinyin.get_pinyin(user.xx.xxmc,u""),role.lower(),klass))
        #path.append(u"%s.roles.%s.%s.%s"%(module_path,Pinyin.get_pinyin(user.xx.xxmc,u""),role.lower(),klass))

    path.append(u"%s.roles.%s.%s"%(app,role.lower(),klass))
    path.append(old_path)


    for p in path:
        try:
            return import_module(p)
        except:
            pass

    return None

def load_member(request,path,role=None):
    m,c = path.rsplit(u".",1)
    return getattr(load_module(request,m,role),c)

#当不提供完整字符路径时在这个字典中查找
models = {
    u"user" : User
}

def load_model(path):
    if models.has_key(path):
        return models[path]

    module,model = path.rsplit(u".",1)
    module = import_module(module)
    return getattr(module,model)

