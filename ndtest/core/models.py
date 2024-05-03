from django.db import models
from datetime import datetime

# Create your models here.

class Alerts(models.Model):
    src_ip=models.CharField(max_length=255)
    dst_ip=models.CharField(max_length=255)
    src_bytes=models.CharField(max_length=255)
    dst_bytes=models.CharField(max_length=255)
    flag=models.CharField(max_length=255)
    service=models.CharField(max_length=255)
    count=models.CharField(max_length=255)
    same_srv_rate=models.CharField(max_length=255)
    diff_srv_rate=models.CharField(max_length=255)
    dst_host_srv_count=models.CharField(max_length=255)
    dst_host_same_srv_rate=models.CharField(max_length=255)
    dst_host_same_src_port_rate=models.CharField(max_length=255)
    datetime=models.CharField(max_length=255,default=datetime.now())

    class Meta:
        db_table='alert'

class TotalDevices(models.Model):
    src_ip=models.CharField(max_length=255)
    dst_ip=models.CharField(max_length=255)
    type=models.CharField(max_length=250,default='normal')
    class Meta:
        db_table='devices'

    



