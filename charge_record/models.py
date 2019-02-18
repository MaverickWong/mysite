from django.db import models
from boards.models import Person
from django.contrib.auth.models import User
# Create your models here.

# {"pageIndex":1,"pageSize":10,"pageCount":1,"totalCount":2,
# "items":[{
#           "chargeOrderDetailList":[],
#           "chargeOrderSimpleDetailList":[
#                   {"chargeOrderId":763209,"sourceDetailId":301128,"chargeType":"正畸费","chargeSuperType":"缺省大类","originalTotalPrice":20000.00,"totalPrice":20000.00,"allowDiscount":true,"discount":100.0,"discountPrice":0.00,"actualPrice":20000.00,"overdue":0.00,"isReimburse":false,"price":20000.00,"doctorId":913,"doctorName":"张栋梁","nurseId":null,"nurseName":"","consultantId":null,"consultantName":"","sellerId":null,"id":301128}],
#           "giftCertificateList":[],
#           "officeAdvancePaymentUsedInfoList":null,
#           "groupBuyCertificateList":null,
#           "chargeDeductionExecution":null,
#           "freeField":null,
#           "id":763209,
#           "appointmentId":1283287,
#           "patientId":446891,
# "memberShipCardId":null,"payOfficeId":122,"giftCertificateId":0,"giftTransactionId":null,
# "sourceChargeOrderId":763209,
# "fromChargeOrderId":0,"giftCardId":0,"insuranceOrderId":null,"yibaoOrderId":0,"officeId":122,"lisOrderId":null,
# "totalPrice":20000.00,"planPrice":20000.00,"actualPrice":20000.00,"overdue":0.00,"discountPrice":0.00,
# "discount":100.0,"payType":"银行卡","actualPrice1":20000.00,"payType2":"","actualPrice2":null,"payType3":"",
# "actualPrice3":null,"recordCreatedTime":"2019-01-06T12:53:30","recordUpdatedTime":"2019-01-06T12:53:30",
# "payDateTime":"2019-01-06T12:53:30","visitingTime":null,"payeeId":2191,"payee":"骆瑞","doctorId":913,
# "doctorName":"张栋梁","nurseId":0,"nurseName":"","consultantId":null,"consultantName":null,"billNo":"0013042",
# "comments":"","authCode":null,"chargePoint":null,"createBy":null,"recordCreatedUser":1429,"overdueStatus":null,
# "reason":null,"status":"已收费","orderType":"simple","isHandle":false,"notUseMembershipDiscount":null,
# "isAppend":false,"feeType":0,"feeSubType":0,"channel":1,"isAliPay":false,"isWeixinPay":false,
# "isNotAutoCheckOut":false,"isArchived":null,"isNeedConfirm":false,"isConfirmed":false,
# "isDefaultDeduction":false,"workflowStatus":null,"deviceCode":null,"lastTimeOverdue":0.0,
# "officeName":null,"isPrompt":false,"allowWeixinBillOrder":false,"openId":null,"isAliPayOrder":null,
# "membershipTransaction":null,"isOldCharge":false,"isPayOverdue":false,"isOldToNew":false},


# 收费总表，记录所有收费大条目，每个收费大条目关联数个细节
class ChargeOrder(models.Model):
	planPrice = models.FloatField(null=True)  # 应收费数目
	inPrice = models.FloatField(null=True)  # 实收
	discount = models.FloatField(null=True)  # 折扣百分数
	createdAt = models.DateTimeField(auto_now_add=True)
	payType = models.CharField(max_length=20, null=True)  # 收费类型，现金，支付宝等

	person = models.ForeignKey(Person, related_name='charge_orders', null=True, on_delete=models.SET_NULL)
	personId = models.PositiveIntegerField(null=True) # 再次记录下personid，保险

	doctor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	# doctor = models.CharField(max_length=20, null=True, blank=True)  # zdl
	# clinic = models.CharField(null=True, max_length=20, blank=True)
	comment = models.CharField(max_length=255, null=True)


# 收费细节，每个收费大条目关联数个细节（为了拔牙，牙刷，药物等单列）
class ChargeDetails(models.Model):
	planPrice = models.FloatField( null=True)  # 应收费数目
	# inPrice = models.PositiveSmallIntegerField()  # 实收
	discount = models.FloatField( null=True)  # 折扣百分数
	createdAt = models.DateTimeField(auto_now_add=True)
	payType = models.CharField(max_length=20, null=True)  # 收费类型，现金，支付宝等
	chargeOrder = models.ForeignKey(ChargeOrder, related_name='charge_details', null=True, on_delete=models.SET_NULL)

	# person = models.ForeignKey('Person', related_name='charge_details', null=True, on_delete=models.SET_NULL)
	personId = models.PositiveIntegerField(null=True)  # 再次记录下personid，保险

	doctor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	# doctor = models.CharField(max_length=20, null=True, blank=True)  # zdl
	clinic = models.CharField(null=True, max_length=20, blank=True)
	comment = models.CharField(max_length=255, null=True)