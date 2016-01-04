#-*- encoding:utf8 -*-

#导入考生语句模版

#从学生表中导入考生
def daorukaosheng_from_xuesheng(kaoshi):
    result = []
    result.append(u'insert into school_kaosheng(kaoshi_id,kaosheng_id,kaochang_id,kaohao)')
    result.append(u'select %s,user.id,0,0'%kaoshi.pk)
    result.append(u'from auth_user as user inner join accounts_banji as banji inner join accounts_nianji as nianji')
    result.append(u'on user.bj_id=banji.id and banji.nj_id=nianji.id')
    result.append(u'where nianji.id = %s'%kaoshi.ksnj.id)
    return u'\n'.join(result)

#从上考生表(Kaosheng)中读取上次参加考试学生名单
def daorukaosheng_from_shangyicikaoshi(kaoshi):
    result = []
    result.append(u'insert into school_kaosheng(kaoshi_id,kaosheng_id,kaochang_id,kaohao)')
    result.append(u'select %s,user.id,0,0'%kaoshi.pk)
    result.append(u'from auth_user as user inner join school_kaosheng as kaosheng inner join accounts_banji as banji inner join accounts_nianji as nianji')
    result.append(u'on user.id = kaosheng.kaosheng_id and user.bj_id=banji.id and banji.nj_id=nianji.id')
    result.append(u'where kaosheng.kaoshi_id=%s and nianji.id=%s'%(kaoshi.sycks.id,kaoshi.ksnj.id))
    return u'\n'.join(result)

