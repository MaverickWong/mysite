from django.db import models
from boards.models import Person
from django.contrib.auth.models import User
# Create your models here.


class ChargeSummary(models.Model):
	"""
	收费统计
	每次收费后一定要创建一个新的
	"""
	person = models.ForeignKey(Person, related_name='charge_summary', on_delete=models.SET_NULL, null=True, blank=True)

	totalPlanPrice = models.FloatField(null=True, default=0)
	totalActualPrice = models.FloatField(null=True, default=0)
	totalOverdue = models.FloatField(null=True, default=0)
	totalAdvacePrice = models.FloatField(null=True, default=0)

	createTime = models.DateTimeField(auto_now_add=True)
	importText = models.CharField(max_length=192, null=True)


class ChargeOrder(models.Model):
	'''
	# 记录所有收费大条目，每个收费大条目关联数个细节
	'''

	totalPrice = models.FloatField(null=True, default=0)
	actualPrice = models.FloatField(null=True, default=0)
	overdue = models.FloatField(null=True, default=0)
	discountPrice = models.FloatField(null=True, default=0)
	discount = models.FloatField(null=True, default=0.0)  # 折扣百分数
	actualPrice1 = models.FloatField(null=True, default=0)
	payType = models.CharField(max_length=24, null=True)  # 收费类型，现金，支付宝等

	recordCreatedTime_text = models.CharField(max_length=32, null=True)  # 2016-04-17T18:51:40
	recordCreatedTime = models.DateTimeField(auto_now_add=True)
	# recordUpdatedTime = models.CharField(max_length=32, null=True)
	# payDateTime = models.CharField(max_length=32, null=True)

	# childChargeOrder = models.One
	# planPrice = models.FloatField(null=True)  # 应收费数目
	# inPrice = models.FloatField(null=True)  # 实收
	# discount = models.FloatField(null=True)  # 折扣百分数

	# createdAt = models.DateTimeField(auto_now_add=True)

	person = models.ForeignKey(Person, related_name='charge_orders', null=True, on_delete=models.SET_NULL)
	personId = models.PositiveIntegerField(null=True)  # 再次记录下personid，保险

	doctor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	doctorId = models.PositiveSmallIntegerField(null=True)
	doctorName = models.CharField(max_length=16, null=True)

	# doctor = models.CharField(max_length=20, null=True, blank=True)  # zdl
	# clinic = models.CharField(null=True, max_length=20, blank=True)
	comments = models.CharField(max_length=128, null=True)

	id2 = models.PositiveSmallIntegerField(null=True)
	appointmentId = models.PositiveSmallIntegerField(null=True)
	patientId = models.PositiveSmallIntegerField(null=True)
	sourceChargeOrderId = models.PositiveSmallIntegerField(null=True)

	status = models.CharField(max_length=24, null=True)
	isAliPay = models.BooleanField(null=True, default=False)
	isWeixinPay = models.BooleanField(null=True, default=False)

	# 是否导入
	import_text = models.CharField(max_length=5120, null=True)
	isImported = models.BooleanField(null=True, default=False)

	''' linkedcare内容
		giftCertificateList	[]
		officeAdvancePaymentUsedInfoList	null
		groupBuyCertificateList	null
		chargeDeductionExecution	null
		freeField	null

		memberShipCardId	null
		payOfficeId	122
		giftCertificateId	null
		giftTransactionId	null
		fromChargeOrderId	0
		giftCardId	null
		insuranceOrderId	null
		yibaoOrderId	0
		tenantId	47d876b6-fc2f-4842-b88e-85ef85425e34
		payType2
		actualPrice2	null
		payType3
		actualPrice3	null
		advancePlanPrice	0
		advancePrice	0
		advanceOverdue	0
		advancePricePaymentTypes	null
		scenario	0

		visitingTime	null
		payeeId	975
		payee	管理员
		nurseId	0
		nurseName
		consultantId	null
		consultantName	null
		billNo	null
		authCode	null
		chargePoint	null
		createBy	null
		recordCreatedUser	-1
		overdueStatus	null
		reason	null
		orderType	simple
		isHandle	null
		notUseMembershipDiscount	false
		isAppend	null
		feeType	0
		feeSubType	0
		channel	0

		isNotAutoCheckOut	false
		isArchived	null
		isNeedConfirm	false
		isConfirmed	false
		isDefaultDeduction	false
		workflowStatus	null
		workflowType	null
		workflowApprovedTime	null
		deviceCode	null
		lastTimeOverdue	0
		officeName	null
		isPrompt	false
		allowWeixinBillOrder	false
		openId	null
		isAliPayOrder	null
		membershipTransaction	null
		isOldCharge	false
		isPayOverdue	false
		isOldToNew	false
	'''


class ChildChargeOrder(models.Model):
	'''
	收据条目item下面的收费账单说明（child-bill）
        例如交了28000，18000是微信，10000是现金
	'''
	# 收费条目item
	sourceChargeOrder = models.ForeignKey(ChargeOrder, related_name='ChildChargeOrders', on_delete=models.SET_NULL,
	                                      null=True)
	# sourceId = models.PositiveSmallIntegerField(null=True)

	totalPrice = models.FloatField(null=True, default=0)
	actualPrice = models.FloatField(null=True, default=0)
	overdue = models.FloatField(null=True, default=0)
	discountPrice = models.FloatField(null=True, default=0)
	discount = models.FloatField(null=True, default=0.0)  # 折扣百分数
	actualPrice1 = models.FloatField(null=True, default=0)
	payType = models.CharField(max_length=24, null=True)  # 收费类型，现金，支付宝等

	recordCreatedTime_text = models.CharField(max_length=32, null=True)  # 2016-04-17T18:51:40
	recordCreatedTime = models.DateTimeField(auto_now_add=True)
	# recordUpdatedTime = models.CharField(max_length=32, null=True)
	# payDateTime = models.CharField(max_length=32, null=True)

	# childChargeOrder = models.One
	# planPrice = models.FloatField(null=True)  # 应收费数目
	# inPrice = models.FloatField(null=True)  # 实收
	# discount = models.FloatField(null=True)  # 折扣百分数

	# createdAt = models.DateTimeField(auto_now_add=True)

	person = models.ForeignKey(Person, related_name='child_orders', null=True, on_delete=models.SET_NULL)
	personId = models.PositiveIntegerField(null=True)  # 再次记录下personid，保险

	doctor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	doctorId = models.PositiveSmallIntegerField(null=True)
	doctorName = models.CharField(max_length=16, null=True)

	# doctor = models.CharField(max_length=20, null=True, blank=True)  # zdl
	# clinic = models.CharField(null=True, max_length=20, blank=True)
	comments = models.CharField(max_length=128, null=True)

	id2 = models.PositiveSmallIntegerField(null=True)
	appointmentId = models.PositiveSmallIntegerField(null=True)
	patientId = models.PositiveSmallIntegerField(null=True)
	sourceChargeOrderId = models.PositiveSmallIntegerField(null=True)

	status = models.CharField(max_length=24, null=True)
	isAliPay = models.BooleanField(null=True, default=False)
	isWeixinPay = models.BooleanField(null=True, default=False)

	# 是否导入
	import_text = models.CharField(max_length=5120, null=True)
	isImported = models.BooleanField(null=True, default=False)


class ChargeDetails(models.Model):
	"""
	# 收费细节，每个收费大条目关联数个细节（为了拔牙，牙刷，药物等单列）
	"""
	planPrice = models.FloatField(null=True)  # 应收费数目
	# inPrice = models.PositiveSmallIntegerField()  # 实收
	discount = models.FloatField(null=True)  # 折扣百分数
	createdAt = models.DateTimeField(auto_now_add=True)
	payType = models.CharField(max_length=20, null=True)  # 收费类型，现金，支付宝等
	chargeOrder = models.ForeignKey(ChargeOrder, related_name='charge_details', null=True, on_delete=models.SET_NULL)

	# person = models.ForeignKey('Person', related_name='charge_details', null=True, on_delete=models.SET_NULL)
	personId = models.PositiveIntegerField(null=True)  # 再次记录下personid，保险

	doctor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	# doctor = models.CharField(max_length=20, null=True, blank=True)  # zdl
	clinic = models.CharField(null=True, max_length=20, blank=True)
	comment = models.CharField(max_length=255, null=True)
