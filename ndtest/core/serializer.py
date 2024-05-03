from rest_framework import serializers
from .models import Alerts,TotalDevices

class  AlertsSerial(serializers.ModelSerializer):
    class Meta:
        model=Alerts
        fields='__all__'

class TotalDevicesSerial(serializers.ModelSerializer):
    class Meta:
        model=TotalDevices
        fields='__all__'