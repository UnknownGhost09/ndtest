
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import joblib
import pandas as pd
from .models import TotalDevices,Alerts
from .serializer import AlertsSerial,TotalDevicesSerial
from asgiref.sync import sync_to_async
model=joblib.load('network.joblib')
service_model=joblib.load('service.joblib')
flag_model=joblib.load('flag.joblib')
class_model = joblib.load('class.joblib')
protocol_type_model=joblib.load('protocol_type.joblib')
import time


def check_packet(d,src_ip,dst_ip):
    
    d['service']=service_model.transform(d['service'])
 
    d['flag']=flag_model.transform(d['flag'])
    print(d['flag'])

    
    prediction=model.predict(d)
    print(prediction)

    try:
        TotalDevices.objects.get(src_ip=src_ip)
    except:
        if prediction[0]==0:
            TotalDevices.objects.create(src_ip=src_ip,dst_ip=dst_ip,type='anomaly')
        else:
            TotalDevices.objects.create(src_ip=src_ip,dst_ip=dst_ip,type='normal')
    
    if prediction[0]==0:
        prediction='anomaly'
        Alerts.objects.create(src_ip=src_ip,dst_ip=dst_ip,src_bytes=d['src_bytes'].values[0],dst_bytes=d['dst_bytes'].values[0],flag=d['flag'].values[0],service=d['service'].values[0],count=d['count'].values[0],same_srv_rate=d['same_srv_rate'].values[0],diff_srv_rate=d['diff_srv_rate'].values[0],dst_host_srv_count=d['dst_host_srv_count'].values[0],dst_host_same_srv_rate=d['dst_host_same_srv_rate'].values[0],dst_host_same_src_port_rate=d['dst_host_same_src_port_rate'].values[0])
    else:
        prediction='normal'
    return prediction

def getdata():
    
    alerts=Alerts.objects.all()
    total_devices=len(TotalDevices.objects.all())
    normal=len(TotalDevices.objects.filter(type='normal'))
    anomaly=len(TotalDevices.objects.filter(type='anomaly'))
    data={"alerts":AlertsSerial(Alerts.objects.all().order_by('-id')[:10],many=True).data,'normal':normal,'anomaly':anomaly,'total_devices':total_devices}
    return data
    


class PacketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "packet"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print('connection created')
        message={"message":"connected"}
        await self.send(json.dumps(message))


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        print(text_data)
        text_data_json = json.loads(text_data)
        d=pd.DataFrame({'service':[text_data_json.get('service')],'flag':[text_data_json.get('flag')],'src_bytes':[text_data_json.get('src_bytes')],'dst_bytes':[text_data_json.get('dst_bytes')],'count':[text_data_json.get('count')],'same_srv_rate':[float(text_data_json.get('same_srv_rate'))/100],'diff_srv_rate':[float(text_data_json.get('diff_srv_rate'))/100],'dst_host_srv_count':[float(text_data_json.get('dst_host_srv_count'))],'dst_host_same_srv_rate':[float(text_data_json.get('dst_host_same_srv_rate'))/100],'dst_host_same_src_port_rate':[float(text_data_json.get('dst_host_same_src_port_rate'))/100]})
        print(d)
        try:
            prediction=await sync_to_async(check_packet, thread_sensitive=True)(d,text_data_json.get('src_ip'),text_data_json.get('dst_ip'))
            text_data_json['type']=prediction
        except:
            text_data_json['type']='normal'
        print('packet recieved-->',text_data_json)
        await self.channel_layer.group_send(
                        self.group_name,
                            {
                                "type": "sending_data",
                                "data":text_data_json
                                            
                            },
                    )
        

    async def sending_data(self, event):
        data=event.get('data')
        await self.send(
            json.dumps(data)
        )
    



class DashboardData(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dashboard"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print('connection created')
        message={"message":"bamal"}
        await self.send(json.dumps(message))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data=await sync_to_async(getdata, thread_sensitive=True)()
        
        time.sleep(2)
        await self.channel_layer.group_send(
                        self.group_name,
                            {
                                "type": "dashboard_data",
                                "data":data               
                            },
                    )
    async def dashboard_data(self, event):
        data=event.get('data')
        await self.send(
            json.dumps(data)
            
        )
    
