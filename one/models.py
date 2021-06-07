from django.db import models

# Create your models here.
"""
创建学生信息表模型
"""

"""
 该类是用来生成数据库的 必须要继承models.Model
"""
class Problem(models.Model):
    """
    创建如下几个表的字段
    """
    # 编号 primary_key=True: 该字段为主键
    id = models.AutoField('编号', primary_key=True)
    # 类型 字符串 最大长度20
    type = models.CharField('类型', max_length=20)
    # 描述 整数 null=False, 表示该字段不能为空
    describe = models.CharField('描述', null=False, max_length=1024)
    # 选项A 布尔类型 默认True: 男生 False:女生
    opA = models.CharField('选项A', max_length=1024)
    # 选项A 布尔类型 默认True: 男生 False:女生
    opB = models.CharField('选项B', max_length=1024)
    # 选项A 布尔类型 默认True: 男生 False:女生
    opC = models.CharField('选项C', max_length=1024)
    # 选项A 布尔类型 默认True: 男生 False:女生
    opD = models.CharField('选项D', max_length=1024)
    # 答案 布尔类型 默认True: 男生 False:女生
    answer = models.CharField('答案', max_length=1024 ,
                              choices=(('A','选项A'),('B','选项B'),('C','选项C'),('D','选项D')))
    # 选项A 布尔类型 默认True: 男生 False:女生
    difficulty = models.IntegerField('难度',
                                     choices=(('0','简单'),('1','困难')))

    # 指定表名 不指定默认APP名字——类名(app_demo_Student)
    class Meta:
        db_table = 'problem'
        ordering = ('id',)


"""
OneToOneField： 一对一
ForeignKey: 一对多
ManyToManyField： 多对多(没有ondelete 属性)
"""
