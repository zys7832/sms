#-*- encoding:utf8 -*-

from . import models

def init():
    for name in dir(models):
        try:
            c = getattr(models,name)
            if hasattr(c,'__bases__') and models.ChoiceModel in c.__bases__:
                print(u'%s开始初始化'%c.__name__)
                c.init()               
        except:
            pass 