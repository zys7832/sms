# -*- encoding:utf8 -*-

from django.db import models
import datas


class ChoiceModel(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'代码')
    name = models.CharField(max_length=200,verbose_name=u'代码值')
    class Meta:
        abstract = True
        
    @classmethod
    def init(cls):
        data_list = list(getattr(datas,cls.__name__.upper()))
        data_list.sort()
        for code,name in data_list:
            cls(code=code,name=name).save()

    def __unicode__(self):
        return u'%s'%self.name

class bxlx(ChoiceModel):
    pass
                
class dwbb(ChoiceModel):
    pass
    
class dwlb(ChoiceModel):
    pass

class szdcxlx(ChoiceModel):
    pass
    
class szdqjjsx(ChoiceModel):
    pass
    
class xxbb(ChoiceModel):
    pass
    
class xxbg(ChoiceModel):
    pass
    
class xxdwcc(ChoiceModel):
    pass
    
class aqjxxs(ChoiceModel):
    pass
    
class byqx(ChoiceModel):
    pass
    
class cfmc(ChoiceModel):  
    pass
    
class cjrlx(ChoiceModel):
    pass
    
class gkkm(ChoiceModel):
    pass

class hjlx(ChoiceModel):
    pass
    
class jdfs(ChoiceModel):
    pass

class jlfs(ChoiceModel):
    pass

class jtlb(ChoiceModel):
    pass

class jxjlx(ChoiceModel):
    pass

class kncd(ChoiceModel):
    pass

class knyy(ChoiceModel):
    pass

class lqlb(ChoiceModel):
    pass

class rxfs(ChoiceModel):
    pass

class tjxmlb(ChoiceModel):
    pass

class wjlb(ChoiceModel):
    pass

class xjydlb(ChoiceModel):
    pass

class xjydyy(ChoiceModel):
    pass

class xsbd(ChoiceModel):
    pass

class xsdqzt(ChoiceModel):
    pass

class xshjlb(ChoiceModel):
    pass

class xslb(ChoiceModel):
    four = 5
    
class xsly(ChoiceModel):
    pass
        
class xstzdb(ChoiceModel):
    pass

class txyy(ChoiceModel):
    pass

class yzblxw(ChoiceModel):
    pass

class zxxxsly(ChoiceModel):
    pass

class be(ChoiceModel):
    pass

class jkrlb(ChoiceModel):
    pass

class jslx(ChoiceModel):
    pass

class jxlx(ChoiceModel):
    pass

class jxyfxz(ChoiceModel):
    pass

class ksfs(ChoiceModel):
    pass

class ksxs(ChoiceModel):
    pass

class ksxz(ChoiceModel):
    pass

class nj(ChoiceModel):
    pass

class rxnl(ChoiceModel):
    pass

class qkwb(ChoiceModel):
    pass

class skfs(ChoiceModel):
    pass

class ssmzsyjxms(ChoiceModel):
    pass

class xq(ChoiceModel):
    pass

class xz(ChoiceModel):
    pass

class yebjlx(ChoiceModel):
    pass

class zsdx(ChoiceModel):
    pass

class zxxbjlx(ChoiceModel):
    pass

class zxxbzlb(ChoiceModel):
    pass

class zxxkc(ChoiceModel):
    pass

class zxxkcdj(ChoiceModel):
    pass

class zxxsylb(ChoiceModel):
    pass

class xb(ChoiceModel):
    pass

class gwzy(ChoiceModel):
    pass

class jshjlb(ChoiceModel):
    pass

class jzgdqzt(ChoiceModel):
    pass

class jzglb(ChoiceModel):
    pass

class jzgly(ChoiceModel):
    pass

class lgyy(ChoiceModel):
    pass

class lxlzyy(ChoiceModel):
    pass

class prqk(ChoiceModel):
    pass

class pyxz(ChoiceModel):
    pass

class rkjs(ChoiceModel):
    pass

class rkxd(ChoiceModel):
    pass

class zwlb(ChoiceModel):
    pass

class gatqw(ChoiceModel):
    pass

class jb(ChoiceModel):
    pass

class jldj(ChoiceModel):
    pass

class pthspdj(ChoiceModel):
    pass

class sfbz(ChoiceModel):
    pass

class sfzjlx(ChoiceModel):
    pass

class shdwxz(ChoiceModel):
    pass

class xx(ChoiceModel):
    pass

class cbsjb(ChoiceModel):
    pass

class cghjlb(ChoiceModel):
    pass

class cglx(ChoiceModel):
    pass

class jdjl(ChoiceModel):
    pass

class jhwcqk(ChoiceModel):
    pass

class js(ChoiceModel):
    pass
    
class kwjb(ChoiceModel):
    pass

class lwbgxs(ChoiceModel):
    pass

class lzlb(ChoiceModel):
    pass

class shjjxy(ChoiceModel):
    pass

class srlx(ChoiceModel):
    pass

class wcxs(ChoiceModel):
    pass

class xkmlkj(ChoiceModel):
    pass

class xmjfly(ChoiceModel):
    pass

class xmlx(ChoiceModel):
    pass

class xmly(ChoiceModel):
    pass

class xmzxzt(ChoiceModel):
    pass

class xshydj(ChoiceModel):
    pass

class xsjllx(ChoiceModel):
    pass

class xsttjb(ChoiceModel):
    pass

class xzdwlx(ChoiceModel):
    pass

class zlflzt(ChoiceModel):
    pass

class zllx(ChoiceModel):
    pass

class zlpzxs(ChoiceModel):
    pass

class gbtkhlb(ChoiceModel):
    pass

class gbtkhjl(ChoiceModel):
    pass

class gbtyzlb(ChoiceModel):
    pass

class gbbzlb(ChoiceModel):
    pass

class gbgwlb(ChoiceModel):
    pass

class gbjtgx(ChoiceModel):
    pass
        
class gbhyzk(ChoiceModel):
    pass

class gbkcdm(ChoiceModel):
    pass

class gbxldm(ChoiceModel):
    pass

class gbzzmm(ChoiceModel):
    pass

class gbxzqh(ChoiceModel):
    pass
    
    
class gbmz(ChoiceModel):
    pass

class gbjkzk(ChoiceModel):
    pass

class gbzjxy(ChoiceModel):
    pass

class gbhkxz(ChoiceModel):
    pass

class gbxwdm(ChoiceModel):
    pass
    
class gbzyjszw(ChoiceModel):
    pass

class gbzwjbm(ChoiceModel):
    pass
    
class zczk(ChoiceModel):
    pass

class gbjypxjg(ChoiceModel):
    pass

class kwzd(ChoiceModel):
    pass

class gbyzlb(ChoiceModel):
    pass

            
        