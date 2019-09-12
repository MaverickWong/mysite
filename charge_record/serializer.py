from rest_framework import serializers
from .models import ChargeOrder


class ChargeOrderSerializer(serializers.ModelSerializer):
	# 自行添加item
	person2 = serializers.ReadOnlyField(source='person.name')

	class Meta:
		model = ChargeOrder
		fields = ('totalPrice', 'actualPrice', 'overdue', 'url', 'person', 'person2', 'doctor')
