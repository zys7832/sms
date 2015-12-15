#-*- encoding : utf8 -*-

from django.db import models as db_models

class TreeForeignKey(db_models.ForeignKey):
    pass

class MyIntegerField(db_models.IntegerField):
    def __init__(self,max_=None,min_=None,*args,**kwargs):
        super(MyIntegerField,self).__init__(*args,**kwargs)
        self.max = max_
        self.min = min_

class MyDecimalField(db_models.DecimalField):
    def __init__(self,max_=None,min_=None,*args,**kwargs):
        super(MyDecimalField,self).__init__(*args,**kwargs)
        self.max = max_
        self.min = min_

class MyFloatField(db_models.FloatField):
    def __init__(self,max_=None,min_=None,*args,**kwargs):
        super(MyFloatField,self).__init__(*args,**kwargs)
        self.max = max_
        self.min = min_

class MyCharFiled(db_models.CharField):
    def __init__(self,to_field=None,min_length=None,*args,**kwargs):
        super(MyCharFiled,self).__init(*args,**kwargs)
        self.to_field = to_field
        self.min_length = min_length
