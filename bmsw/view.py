from django.shortcuts import render
from .utils.rfc import *
import pandas as pd
app_name = 'bmsw'
def index(request):
        return render(request,"views/index.html")
def login(request):
        zone_list=read_zone()
        return render(request,"views/main.html",{'zone_list':zone_list})
def insert(request):
        excel_raw_data = pd.read_excel(request.FILES.get('excelFile'))
        for i in range(len(excel_raw_data['主机记录'])):
                print(excel_raw_data['主机记录'][i],excel_raw_data['记录值'][i])
                create_named(Named(excel_raw_data['主机记录'][i], "60", excel_raw_data['记录值'][i])) 
                zone = Zone(excel_raw_data['主机记录'][i]+".fuyoukache.com","master",excel_raw_data['主机记录'][i]+".fuyoukache.com.zone","","","")
                insert_zone(zone)
        return render(request,"views/main.html",{"message":"success"})
def delete(request):
        zone_name = request.GET.get('name')
        delete_zone(zone_name)
        return render(request,"views/main.html",{"message":"success"})
def main(request):
        zone_list=read_zone()
        return render(request,"views/main.html",{'zone_list':zone_list})
