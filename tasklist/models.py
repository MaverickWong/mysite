from django.db import models
from boards.models import Person
# Create your models here.

class Task(models.Model):
    status_choice = (
        (0, '状态'),
        (1, '要做'),
        (2, '已发送'),
        (3, '已收到'),
        (4, '已戴走'),
    )
    group_choice = (
        ('default', '默认'),
        ('shece', '舌侧'),
        ('lucy', 'Lucy透明矫治器-李志鹏'),
        ('chunce', '唇侧计算机定位'),
        ('tpa', '打印TPA'),
        ('shececongzuo', '脱落舌侧托槽重新打印-甄浩'),
        ('shecezhenhao', '舌侧矫治器-甄浩'),
        ('baochiqi', '保持器机加工-马晨'),
        ('jianjie', '间接粘接-李志鹏'),
        ('yinshimei', '隐适美-李志鹏'),
        ('gongneng', '功能矫治器-韩彬羽'),
    )

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='项目名称')
    comment = models.TextField(max_length=200, null=True, blank=True)
    group = models.CharField(choices=group_choice, max_length=20,null=True, blank=True)
    status = models.PositiveIntegerField(choices=status_choice, null=True, blank=True)

    person = models.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
    doc = models.CharField(max_length=20, null=True, blank=True)

    startTime = models.DateField(auto_now_add=True, null=True, blank=True)
    endTime = models.DateField(null=True)
    timeLength = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Task_tags(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='标签名称')
    tasks = models.ManyToManyField(Task, related_name='tags')

    def __str__(self):
        return self.name


