#-*- encoding:utf8 -*-
from django.db import models as db_models,connection
from collections import OrderedDict

class MakeExaminationNumer(object):
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
            self.__seat_count = int(self.exam.kaochang_set.arragate(sum=db_models.Sum('renshu'))[u'sum'])
        return self.__seat_count

    #每个班级考试人数
    @property
    def size_of_classes(self):
        if not self.__size_of_classes:
            sqls = []
            sqls.append(u'select bj.id,count(*) as cnt from accounts_banji as bj inner join school_kaosheng as ks inner join auth_user as user')
            sqls.append(u'on ks.kaosheng_id=user.id and user.bj_id = bj.id')
            sqls.append(u'where ks.kaoshi_id=%s'%self.kaoshi.id)
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
            sqls.append(u'select ks.id from school_kaosheng as ks inner auth_user as user')
            sqls.append(u'on ks.kaosheng_id = user.id')
            sqls.append(u'where ks.kaoshi_id=%s and user.bj_id=%s')
            sqls = u'\n'.join(sqls)
            for cls in self.size_of_classes.keys():
                cursor = connection.cursor()
                cursor.execute(sqls%(self.kaoshi.id,cls))
                self.__examinee_ids_by_class[cls] = [row[0] for row in cursor.fetchall()]
        return self.__examinee_ids_by_class

    def sorted(self):
        result = []
        start_index = 0
        ids = self.examinee_ids_by_class
        size_of_classes_sorted = sorted(self.size_of_classes.items(),key=lambda e:e[1])
        for cls,size in size_of_classes_sorted:
            params = [item[start_index:size] for item in ids.values]
            result.extend(zip(*params))
            start_index = size
            del ids[cls]

        #在result列表中未分隔开的ID起始索引是start_index的最后值
        #获取没有成功分隔的ID列表
        weifenge_id = result[start_index:]
        #删除result中未成功分隔的考生ID
        del result[start_index:]
        class_position = self.examinee_ids_by_class.keys().index(cls)
        start_insert_index = size_of_classes_sorted[-2][1]
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
                current_zu_value.insert(insert_position,weifenge_id.pop(0))
                if not weifenge_id:
                    break;
            result[start_insert_index] = current_zu_value
            start_insert_index -= 1


#插入方法
def insert(li,p,value):
     old_len = len(li)
     for ind in range(old_len-2):
             p += 2
             if p>=len(li):
                     p-=len(li)
             li.insert(p,value)
     print(li)

