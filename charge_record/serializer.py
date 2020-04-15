from rest_framework import serializers
from .models import ChargeOrder, ChargeSummary


class ChargeOrderSerializer(serializers.ModelSerializer):
	# 自行添加item
	person2 = serializers.ReadOnlyField(source='person.name')
	# id = serializers.ReadOnlyField(source='person.name')
	class Meta:
		model = ChargeOrder
		fields = ('id', 'totalPrice', 'actualPrice', 'overdue', 'person2')
		# , 'url', 'person', 'person2', 'doctor'


class ChargeSummarySerializer(serializers.ModelSerializer):
	# 自行添加item
	# person2 = serializers.ReadOnlyField(source='person.name')
	# id = serializers.ReadOnlyField(source='pk')

	class Meta:
		model = ChargeSummary
		fields = ('id','totalPlanPrice', 'totalActualPrice', 'totalOverdue', 'totalAdvacePrice',
		          'createTime', 'importText', 'person')
