from django.db import models
from boards.models import Person
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class DrugItem(models.Model):
	big_group_choice = (
		(0, '分类'),
		(1, '分类1'),
		(2, '分类1'),
		(3, '分类1'),
		(4, '分类1'),
	)
	status_choice = (
		(0, ''),
		(1, '充足'),
		(2, '待补充'),
		(3, '缺货'),
		(4, '分类1'),
	)
	small_group_choice = (
		('default', '无'),
		('shece', '分类1'),
		('lucy', '分类1'),
		('chunce', '分类1'),
		('tpa', '分类1'),
		('shececongzuo', '分类1'),
		('shecezhenhao', '分类1'),
		('baochiqi', '分类1'),
		('jianjie', '分类1'),
		('yinshimei', '分类1'),
		('gongneng', '分类1'),
	)

	name = models.CharField(max_length=100, null=True, blank=True, verbose_name='项目名称')
	shortname = models.CharField(max_length=10, null=True, blank=True, verbose_name='项目名称')
	count = models.PositiveIntegerField(null=True, blank=True)
	min_count = models.PositiveIntegerField(null=True, blank=True)
	comment = models.TextField(max_length=200, null=True, blank=True)

	small_group = models.CharField(choices=small_group_choice, max_length=20, null=True, blank=True)
	big_group = models.PositiveIntegerField(choices=big_group_choice, null=True, blank=True)
	status = models.PositiveIntegerField(choices=status_choice, null=True, blank=True)

	# person = models.ForeignKey(Person, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL)
	# doc = models.CharField(max_length=20, null=True, blank=True)

	cTime = models.DateField(auto_now_add=True, null=True, blank=True)

	# endTime = models.DateField(null=True)
	# timeLength = models.CharField(max_length=10, null=True, blank=True)

	def __str__(self):
		return self.name


#
# class Task_tags(models.Model):
#     name = models.CharField(max_length=50, null=True, blank=True, verbose_name='标签名称')
#     tasks = models.ManyToManyField(Task, related_name='tags')
#
#     def __str__(self):
#         return self.name
#
#


class InOutDetail(models.Model):
	"""
    in out detail
    """

	PROP = (
		('+', _("入库")),
		('-', _("出库"))
	)

	create_time = models.DateTimeField(_("create time"), auto_now_add=True)
	# status = models.BooleanField(_("executed"), default=0)
	event_time = models.DateTimeField(_("event time"), blank=True, null=True)
	drugitem = models.ForeignKey(DrugItem, related_name='inout_details', on_delete=models.CASCADE)

	# warehouse = models.ForeignKey(Warehouse,on_delete=models.CASCADE, verbose_name=_("warehouse"),blank=True,null=True)
	# material = models.ForeignKey(Material,on_delete=models.CASCADE, verbose_name=_("material"),limit_choices_to={"is_virtual":"0"},blank=True,null=True)
	# measure = models.ForeignKey(Measure, on_delete=models.CASCADE, verbose_name=_(
	#     "measure"), blank=True, null=True)
	count = models.DecimalField(_("count"), max_digits=14, decimal_places=4, blank=True, null=True)
	# batch = models.CharField(_("batch"),max_length=const.DB_CHAR_NAME_20,blank=True,null=True)
	price = models.DecimalField(_("price"), max_digits=14, decimal_places=4, blank=True, null=True)
	prop = models.CharField(_("plus or minus property"), max_length=2, choices=PROP, default='+')

	user = models.CharField(max_length=12, blank=True, null=True)
	comment = models.CharField(max_length=64, blank=True, null=True)
