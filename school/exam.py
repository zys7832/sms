#-*- encoding:utf8 -*-
from django.db import models as db_models,connection
from collections import OrderedDict

class MakeExaminationNumber(object):
    def __init__(self,exam):
        self.exam = exam
        self.__examinee_count = 0
        self.__seat_count = 0
        self.__size_of_classes = OrderedDict()
        self.__examinee_ids_by_class = OrderedDict()
    #考生数量
    @property
    def examinee_count(self):
        if self.__examinee_count == 0:
            self.__examinee_count = self.exam.kaosheng_set.count()
        return self.__examinee_count

    #座位数
    @property
    def seat_count(self):
        if self.__seat_count==0:
            try:
                self.__seat_count = int(self.exam.kaoshikaochang_set.aggregate(sum=db_models.Sum('kaoshengshu'))[u'sum'])
            except:
                pass
        return self.__seat_count

    #每个班级考试人数
    @property
    def size_of_classes(self):
        if not self.__size_of_classes:
            sqls = []
            sqls.append(u'select bj.id,count(*) as cnt from accounts_banji as bj inner join school_kaosheng as ks inner join auth_user as user')
            sqls.append(u'on ks.kaosheng_id=user.id and user.bj_id = bj.id')
            sqls.append(u'where ks.kaoshi_id=%s'%self.exam.id)
            sqls.append(u'group by bj.id')
            sqls.append(u'order by bj.order ')
            cursor = connection.cursor()
            cursor.execute(u'\n'.join(sqls))
            self.__size_of_classes = OrderedDict(cursor.fetchall())

        return self.__size_of_classes

    #每班考生ID字典，key为班级ID,值为该班级的考生ID列表
    @property
    def examinee_ids_by_class(self):
        if not self.__examinee_ids_by_class:
            sqls = []
            sqls.append(u'select ks.id from school_kaosheng as ks inner join auth_user as user')
            sqls.append(u'on ks.kaosheng_id = user.id')
            sqls.append(u'where ks.kaoshi_id=%s and user.bj_id=%s')
            sqls = u'\n'.join(sqls)
            for cls in self.size_of_classes.keys():
                cursor = connection.cursor()
                cursor.execute(sqls%(self.exam.id,cls))
                self.__examinee_ids_by_class[cls] = [row[0] for row in cursor.fetchall()]
        return self.__examinee_ids_by_class

    def get_examinee_sorted(self):
        result = []
        start_index = 0
        ids = self.examinee_ids_by_class
        size_of_classes_sorted = sorted(self.size_of_classes.items(),key=lambda e:e[1])
        for cls,size in size_of_classes_sorted:
            params = [item[start_index:size] for bj,item in ids.items()]
            result.extend(zip(*params))
            start_index = size
            del ids[cls]

        #在result列表中未分隔开的ID起始索引是start_index的最后值
        #获取没有成功分隔的ID列表
        weifenge_id = result[size_of_classes_sorted[-2][1]:]
        #删除result中未成功分隔的考生ID
        del result[size_of_classes_sorted[-2][1]:]
        class_position = self.examinee_ids_by_class.keys().index(cls)
        start_insert_index = size_of_classes_sorted[-3][1]
        start_insert_index -= 1 #退到上一个组
        current_length = 0
        current_position = 0
        while weifenge_id :
            zuchang = len(result[start_insert_index])
            if zuchang!=current_length:
                current_length = zuchang
                current_position = 0
                for cls,size in size_of_classes_sorted[zuchang*-1:-1]:
                    if self.examinee_ids_by_class.keys().index(cls)<class_position:
                        current_position+=1
            insert_position = current_position

            current_zu_value = list(result[start_insert_index])
            for index in range(zuchang-2):
                insert_position += 2
                if insert_position>=len(current_zu_value):
                    insert_position = insert_position-len(current_zu_value)
                current_zu_value.insert(insert_position,weifenge_id.pop(0)[0])
                if not weifenge_id:
                    break;
            result[start_insert_index] = current_zu_value
            start_insert_index -= 1
        r1 = []
        for item in result:
            r1.extend(item)

        return r1

    def get_kaochang_list(self):
        result = []
        kaochang_s = self.exam.kaoshikaochang_set.all()
        for kaochang in kaochang_s:
            result.extend([kaochang.id]*kaochang.kaoshengshu)
        return result

    def get_kaohao_list(self):
        result = []
        for kaochang in self.exam.kaoshikaochang_set.all():
            result.extend(range(1,kaochang.kaoshengshu+1))

        return result

    def make_examination_number(self):
        if self.examinee_count>self.seat_count:
            raise Exception(u'现有%s名考生，而座位只有%s个,请在考场设置中做适当调整。'%(self.examinee_count,self.seat_count))
        result = []
        return zip(self.get_kaochang_list()[:self.examinee_count],self.get_kaohao_list()[:self.examinee_count],self.get_examinee_sorted())

    def update_kaohao(self):
        sql = u'update school_kaosheng set kaochang_id=%s,kaohao=%s where id=%s'
        sqls = [sql%value for value in self.make_examination_number()]
        cursor = connection.cursor()
        cursor.execute(u';'.join(sqls))
        return True


#插入方法
def insert(li,p,value):
     old_len = len(li)
     for ind in range(old_len-2):
             p += 2
             if p>=len(li):
                     p-=len(li)
             li.insert(p,value)
     print(li)

