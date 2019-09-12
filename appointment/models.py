from django.db import models
from boards.models import Person
from django.contrib.auth.models import User

# Create your models here.

status = (
	(1, 'isCancel'),
	(2, 'isCheckedIn'),
	(3, 'isFinished'),
	(4, 'isLeft'),
	(5, 'isConfirmed'),
	(6, 'isCheckedOut'),
	(7, 'isFail'),
	(8, 'isPending'),
)


class ApptItem(models.Model):
	dateForAppt = models.ForeignKey('DateForAppoint', related_name='apptItems', null=True, on_delete=models.SET_NULL)
	doctor = models.ForeignKey(User, related_name='apptItems', null=True, on_delete=models.SET_NULL)
	doctorName = models.CharField(max_length=16, null=True)
	patient = models.ForeignKey(Person, related_name='apptItems', null=True, on_delete=models.SET_NULL)
	patientName = models.CharField(max_length=16, null=True)

	# startDate = models.DateField()
	startDateTime = models.DateTimeField(null=True, blank=True)
	endDateTime = models.DateTimeField(null=True, blank=True)
	createDateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	assistantId = models.IntegerField(null=True, blank=True)
	assistantName = models.CharField(max_length=16, null=True)

	comment = models.TextField(max_length=100, null=True, blank=True)

	# status = models.IntegerField(choices=status, null=False, blank=True)
	# 复诊
	type = models.IntegerField(null=True, blank=True)
	isFirstVisit = models.BooleanField(null=True, blank=True, default=False)
	isCharged = models.BooleanField(null=True, blank=True, default=False)
	isRecoded = models.BooleanField(null=True, blank=True, default=False)
	hasRevisit = models.BooleanField(null=True, blank=True, default=False)

	linkedApptID = models.IntegerField(null=True, blank=True)

	# 就诊状态
	isCheckedIn = models.BooleanField(null=True, blank=True, default=False)
	checkInTime = models.DateTimeField(null=True, blank=True)
	checkInType = models.CharField(max_length=16, null=True, blank=True, )
	isCheckedOut = models.BooleanField(null=True, blank=True, default=False)
	isSeated = models.BooleanField(null=True, blank=True, default=False)
	seatTime = models.DateTimeField(null=True, blank=True)

	isCancel = models.BooleanField(null=True, blank=True, default=False)
	isFinished = models.BooleanField(null=True, blank=True, default=False)
	isLeft = models.BooleanField(null=True, blank=True, default=False)
	isConfirmed = models.BooleanField(null=True, blank=True, default=False)
	isFail = models.BooleanField(null=True, blank=True, default=False)
	isPending = models.BooleanField(null=True, blank=True, default=False)

	def __str__(self):
		return str(self.patient.name)


class DateForAppoint(models.Model):
	date = models.DateField(null=True)

	def __str__(self):
		return str(self.date)
