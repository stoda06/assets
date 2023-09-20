import pandas as pd
import os
from django.conf import settings
#import pythoncom
from django.utils.safestring import mark_safe

from django.core import serializers

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import psutil
import platform

from .models import *

from datetime import date

#pip install WMI

import re


today = date.today()

from django.template import RequestContext

# Create your views here.

def dashboard(request):
    return render(request, 'index.html', context={})


def report(request):
    Laptop_data_report = Laptops_records.objects.all()
    print(Laptop_data_report)

    Laptop_data_report_data = list(Laptop_data_report.values())
    Laptop_data_report_df = pd.DataFrame.from_records(Laptop_data_report_data)

    Laptop_data_table = Laptop_data_report_df.to_html(index=False)
    print(Laptop_data_table)

    return render(request, 'reports.html', context={'Laptop_data_table':Laptop_data_table})



def asset(request):
    location_name = location_details.objects.all()
    LapMake = Lapmake_details.objects.all()
    MobMake = Mobmake_details.objects.all()

    Laptop_data = Laptops_records.objects.all()
    print(Laptop_data)

    user = request.user
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name +' '+ last_name
    print('its Username',first_name)
    print('its Username', last_name)
    print(full_name)

    context = {'user': user,
               'first_name': first_name,
               'last_name': last_name,
               'location_name': location_name,
               'LapMake': LapMake,
               'MobMake': MobMake,
               'Laptop_data': Laptop_data,
               }
    return render(request, 'laptop_asset.html', context)

@csrf_exempt
def Laptops_data(request):
    if request.method == "POST":
        temp = request.POST.get('temp')

        LapMake = request.POST.get('inputLapMake')
        if not LapMake:
            return JsonResponse({"error": 'error','txt_black_error':'Make'})

        LapModel = request.POST.get('inputLapModel')
        if not LapModel:
            return JsonResponse({"error": 'error','txt_black_error':'Model'})

        LapRAM = request.POST.get('inputLapRAM')
        if not LapRAM:
            return JsonResponse({"error": 'error', 'txt_black_error': 'RAM'})
        elif int(LapRAM) > 100:
            return JsonResponse({"RAM_Greater": 'RAM_Greater', 'txt_black_error': 'RAM'})
        elif int(LapRAM) < 1:
            return JsonResponse({"RAM_lower": 'RAM_lower', 'txt_black_error': 'RAM'})

        HDDType = request.POST.get('inputLapHDDType')

        LapHDD = request.POST.get('inputLapHDD')
        if not LapHDD:
            return JsonResponse({"error": 'error','txt_black_error':'HDD'})
        elif (int(LapHDD) < 100 or int(LapHDD) > 5000) and HDDType == 'GB':
            return JsonResponse({'HDD_ERROR':'HDD_ERROR','txt_black_error':'HDD'})
        elif int(LapHDD) > 5 and HDDType == 'TB':
            return JsonResponse({'HDD_ERROR':'HDD_ERROR','txt_black_error':'HDD'})

        #HDD Size should be Greater than 100 GB And less than 5TB (5000 GB)


        LapProcessor = request.POST.get('inputLapProcessor')
        if not LapProcessor:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Processor'})

        Lappurchasedate = request.POST.get('inputLappurchasedate')
        if not Lappurchasedate:
            Lappurchasedate = None

        LapSerialNo = request.POST.get('inputLapSerialNo')
        if not LapSerialNo:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Serial Number'})

        Lapassetid = request.POST.get('inputLapassetid')
        if not Lapassetid:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Asset'})

        Lapuname = request.POST.get('inputLapuname')

        LapHDD = LapHDD +' '+ HDDType

        condition1 = Q(Lapassetid=Lapassetid)
        condition2 = Q(Lapuname=Lapuname)
        combined_condition = condition1 | condition2

        if Laptops_records.objects.filter(combined_condition).exists():
            return JsonResponse({'exists': 'exists'})
        else:
            a = Laptops_records(LapMake=LapMake, LapModel=LapModel, LapRAM=LapRAM,LapHDD=LapHDD,LapProcessor=LapProcessor,Lappurchasedate=Lappurchasedate,LapSerialNo=LapSerialNo,Lapassetid=Lapassetid,Lapuname=Lapuname)
            a.save()
            return JsonResponse({'success': 'success', 'sys': 'sys_name'})




def MAC_Laptops_data(request):
    if request.method == "POST":
        temp = request.POST.get('temp')

        MAC_Make = request.POST.get('MACinputLapManufacturer')
        if not MAC_Make:
            return JsonResponse({"error": 'error','txt_black_error':'Make'})

        MAC_Model = request.POST.get('MACinputLapModel')
        if not MAC_Model:
            return JsonResponse({"error": 'error','txt_black_error':'Model'})

        MAC_RAM = request.POST.get('MACinputLapRAM')
        if not MAC_RAM:
            return JsonResponse({"error": 'error', 'txt_black_error': 'RAM'})
        elif int(MAC_RAM) > 100:
            return JsonResponse({"RAM_Greater": 'RAM_Greater', 'txt_black_error': 'RAM'})
        elif int(MAC_RAM) < 1:
            return JsonResponse({"RAM_lower": 'RAM_lower', 'txt_black_error': 'RAM'})

        MAC_HDDType = request.POST.get('MACinputLapHDDType')

        MAC_HDD = request.POST.get('MACinputLapHDD')
        if not MAC_HDD:
            return JsonResponse({"error": 'error','txt_black_error':'HDD'})
        elif (int(MAC_HDD) < 100 or int(MAC_HDD) > 5000) and MAC_HDD == 'GB':
            return JsonResponse({'HDD_ERROR':'HDD_ERROR','txt_black_error':'HDD'})
        elif int(MAC_HDD) > 5 and MAC_HDD == 'TB':
            return JsonResponse({'HDD_ERROR':'HDD_ERROR','txt_black_error':'HDD'})

        #HDD Size should be Greater than 100 GB And less than 5TB (5000 GB)


        MAC_Processor = request.POST.get('MACinputLapProcessor')
        if not MAC_Processor:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Processor'})

        MAC_purchasedate = request.POST.get('MACinputLappurchasedate')
        if not MAC_purchasedate:
            MAC_purchasedate = None

        MAC_SerialNo = request.POST.get('MACinputLapSerialNo')
        if not MAC_SerialNo:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Serial Number'})

        MAC_assetid = request.POST.get('MACinputLapassetid')
        if not MAC_assetid:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Asset'})

        MAC_uname = request.POST.get('MACinputLapuname')

        MAC_HDD = MAC_HDD +' '+ MAC_HDDType

        print('before condition ')

        print('Asset ID',MAC_assetid)
        print('Uname IS', MAC_uname)

        condition1 = Q(Lapassetid=MAC_assetid)
        condition2 = Q(Lapuname=MAC_uname)
        combined_condition = condition1 | condition2

        if Laptops_records.objects.filter(combined_condition).exists():
            return JsonResponse({'exists': 'exists'})


        else:
            print('Before Saving')
            a = Laptops_records(LapMake=MAC_Make, LapModel=MAC_Model, LapRAM=MAC_RAM,LapHDD=MAC_HDD,LapProcessor=MAC_Processor,
                                Lappurchasedate=MAC_purchasedate,LapSerialNo=MAC_SerialNo,Lapassetid=MAC_assetid,Lapuname=MAC_uname)
            a.save()
            print('its Saved')
            return JsonResponse({'success': 'success', 'sys': 'sys_name'})



from django.shortcuts import render
import subprocess


def laptop_configuration(request):
    if request.method == "POST":
        location_name = request.POST.get('location_name')
        Lapuname = request.POST.get('inputLapuname')
        print('its uname from laptop config',Lapuname)
        print(location_name)
        script_path = os.path.join(settings.BASE_DIR, 'assets', 'autoload.ps1')
        print(script_path)

        # Run the PowerShell script using subprocess
        powershell_script = """
            # Get general system information
        $systemInfo = Get-CimInstance -ClassName Win32_ComputerSystem
        
        # Get processor information
        $processorInfo = Get-CimInstance -ClassName Win32_Processor
        
        # Get memory (RAM) information
        $memoryInfo = Get-CimInstance -ClassName Win32_PhysicalMemory
        
        # Get disk drive information
        $diskInfo = Get-CimInstance -ClassName Win32_DiskDrive
        
        # Get laptop serial number from Win32_BIOS
        $serialNumber = (Get-CimInstance -ClassName Win32_BIOS).SerialNumber
        
        # Get network adapter information
        $networkInfo = Get-CimInstance -ClassName Win32_NetworkAdapterConfiguration | Where-Object { $_.IPAddress -ne $null }
        
        # Calculate the total memory capacity
        $totalMemoryCapacity = ($memoryInfo | Measure-Object -Property Capacity -Sum).Sum
        
        # Display the collected information
        Write-Host "System Information"
        Write-Host "------------------"
        Write-Host "Manufacturer: $($systemInfo.Manufacturer)"
        Write-Host "Model: $($systemInfo.Model)"
        Write-Host "Processor: $($processorInfo.Name)"
        Write-Host "Serial Number: $serialNumber"
        Write-Host "Memory: $($totalMemoryCapacity / 1GB) GB"
        Write-Host "Disk Drive:"
        foreach ($drive in $diskInfo) {
            Write-Host "  - Model: $($drive.Model)"
            Write-Host "  - Size: $($drive.Size / 1GB) GB"
        }
        Write-Host "Network Adapter:"
        foreach ($adapter in $networkInfo) {
            Write-Host "  - Description: $($adapter.Description)"
            Write-Host "  - IP Address: $($adapter.IPAddress)"
        }   
            """
        print('before inupt string')

#        input_string  subprocess.check_output(['pwsh', '-ExecutionPolicy', 'Bypass', '-Command', powershell_script], text=True)
#        input_string1 = subprocess.call(['pwsh', '-File', script_path], capture_output=True, text=True)
 #       input_string = input_string1.stdout
       # print('after input string')
        input_string = subprocess.check_output(['powershell', '-File', script_path], shell=True,text=True)
        print('after input string')

        print(input_string)
        # Define regular expressions for each piece of informatio
        manufacturer_pattern = r"Manufacturer:\s+(.*)"
        model_pattern = r"Model:\s+(.*)"
        processor_pattern = r"Processor:\s+(.*)"
        serial_number_pattern = r"Serial Number:\s+(\S+)"
        memory_pattern = r"Memory:\s+([\d.]+)\s+GB"
        disk_drive_pattern = r"- Model:\s+(.*?)\n\s+- Size:\s+([\d.]+)\s+GB"
        network_adapter_pattern = r"- Description:\s+(.*?)\n\s+- IP Address:\s+(.*?)\n"

        print('after RE pattern')

        # Find matches using regular expressions
        manufacturer_match = re.search(manufacturer_pattern, input_string)
        model_match = re.search(model_pattern, input_string)
        processor_match = re.search(processor_pattern, input_string)
        serial_number_match = re.search(serial_number_pattern, input_string)
        memory_match = re.search(memory_pattern, input_string)
        disk_drive_matches = re.findall(disk_drive_pattern, input_string)
        network_adapter_matches = re.findall(network_adapter_pattern, input_string)
        print('after RE match')

        # Extract information from matches
        manufacturer = manufacturer_match.group(1) if manufacturer_match else None
        model = model_match.group(1) if model_match else None
        processor = processor_match.group(1) if processor_match else None
        serial_number = serial_number_match.group(1) if serial_number_match else None
        memory = memory_match.group(1) if memory_match else None
        #disk_drive_info = [{"Model": m[0], "Size": m[1]} for m in disk_drive_matches]
        #disk_drive_info = [{"Model": m[0], "Size": round(float(m[1]), 2)} for m in disk_drive_matches]
        print('after RE group')
        disk_drive_info = [{"Model": m[0], "Size": round(float(m[1]))} for m in disk_drive_matches]

        network_adapter_info = [{"Description": na[0], "IP Address": na[1]} for na in network_adapter_matches]
        print(manufacturer)

        serial_no = serial_number
        print(serial_no)
        sliced_serial_number = serial_no[-5:]
        asset_id = f'LPT{location_name}{sliced_serial_number}'

        print(serial_no)
        print(location_name)
        print(asset_id)

        memory = memory + " GB"

        print(memory)

        # Define the context data to pass to the template
        context = {
            'manufacturer': manufacturer,
            'model': model,
            'processor': processor,
            'serial_no': serial_no,
            'memory': memory,
            'disk_drive_info': disk_drive_info,
            'network_adapter_info': network_adapter_info,
            'asset_id':asset_id,
            'Lapuname':Lapuname,

        }

        print(context)

        for entry in disk_drive_info:
            size = str(entry["Size"]) + " GB"
            print(size)

        condition1 = Q(Lapassetid=asset_id)
        condition2 = Q(Lapuname=Lapuname)
        combined_condition = condition1 | condition2

        if Laptops_records.objects.filter(combined_condition).exists():
            #laptop_user_data  = Laptops_records.objects.all()
            existed_data = Laptops_records.objects.filter(combined_condition)
            existed_data_df = pd.DataFrame.from_records(existed_data.values())
            print(existed_data_df)
            existed_data_df = existed_data_df.drop(columns=existed_data_df.columns[:1])

            existed_data_df.rename(columns={'Lapassetid': 'Asset ID', 'LapSerialNo': 'Serial Number',
                                            'Lapassetid': 'Asset ID', 'LapSerialNo': 'Serial Number',
                                            'LapMake': 'Manufacturer', 'LapModel': 'Laptop Model',
                                            'LapRAM': 'RAM', 'LapHDD': 'Hard disk',
                                            'LapProcessor': 'Processor', 'Lappurchasedate': 'Purchase date',
                                            'Lapuname': 'User Name '
                                            }, inplace=True)

            #existed_data_df.rename({'Asset ID', '1','2','3','4','5','6','7','8','9'}, axis=1, inplace=True)

            #existed_data_df = ['Asset ID', '1','2','3','4','5','6','7','8','9']
            #existed_data_df.columns = existed_data_df
            #laptop_user_data_df = pd.DataFrame.from_records(laptop_user_data.values())
            existed_data_df_html = existed_data_df.to_html(classes='table table-striped',justify='center',col_space=15)



            return JsonResponse({'exists': 'exists','existed_data_df_html':existed_data_df_html})
        else:
            a = Laptops_records(LapMake=manufacturer, LapModel=model, LapRAM=memory, LapHDD=size, LapProcessor=processor,
                            Lappurchasedate='2023-03-27', LapSerialNo=serial_no, Lapassetid=asset_id,
                            Lapuname=Lapuname)
            a.save()
            return JsonResponse(context)






# def Laptops_data(request):
#     if request.method == "POST":
#         temp = request.POST.get('temp')
#         LapMake = request.POST.get('inputLapMake')
#         print(LapMake)
#
#         if not LapMake:
#             return JsonResponse({"error": 'error','txt_black_error':'Make'})
#
#         LapModel = request.POST.get('inputLapModel')
#         if not LapModel:
#             return JsonResponse({"error": 'error','txt_black_error':'Model'})
#
#         LapRAM = request.POST.get('inputLapRAM')
#         if not LapRAM:
#             return JsonResponse({"error": 'error', 'txt_black_error': 'RAM'})
#         elif int(LapRAM) > 100:
#             return JsonResponse({'error':'error',"RAM_Greater": 'RAM_Greater', 'txt_black_error': 'RAM'})
#
#         HDDType = request.POST.get('inputLapHDDType')
#
#         LapHDD = request.POST.get('inputLapHDD')
#
#         if not LapHDD:
#             return JsonResponse({"error": 'error','txt_black_error':'HDD'})
#
#         LapProcessor = request.POST.get('inputLapProcessor')
#         if not LapProcessor:
#             return JsonResponse({"error": 'error', 'txt_black_error': 'Processor'})
#
#         Lappurchasedate = request.POST.get('inputLappurchasedate')
#         if not Lappurchasedate:
#             Lappurchasedate = None
#
#         LapSerialNo = request.POST.get('inputLapSerialNo')
#         if not LapSerialNo:
#             return JsonResponse({"error": 'error', 'txt_black_error': 'Serial Number'})
#
#         Lapassetid = request.POST.get('inputLapassetid')
#         if not Lapassetid:
#             return JsonResponse({"error": 'error', 'txt_black_error': 'Asset'})
#
#         Lapuname = request.POST.get('inputLapuname')
#
#         condition1 = Q(Lapassetid=Lapassetid)
#         condition2 = Q(Lapuname=Lapuname)
#
#         combined_condition = condition1 | condition2
#
#         #if Laptops_records.objects.filter(combined_condition).exists():
#          #   print('record exists')
#           #  return JsonResponse({'exists': 'exists'})
#         #else:
#
#         LapHDD = LapHDD +' '+ HDDType
#         a = Laptops_records(LapMake=LapMake, LapModel=LapModel, LapRAM=LapRAM,LapHDD=LapHDD,LapProcessor=LapProcessor,Lappurchasedate=Lappurchasedate,LapSerialNo=LapSerialNo,Lapassetid=Lapassetid,Lapuname=Lapuname)
#         a.save()
#         return JsonResponse({'success': 'success', 'sys': 'sys_name'})
#


def Mobile_data(request):
    if request.method == "POST":
        temp = request.POST.get('temp')

        MobMake = request.POST.get('inputMobMake')
        if not MobMake:
            return JsonResponse({"error": 'error','txt_black_error':'Make'})

        MobModel = request.POST.get('inputMobModel')
        if not MobModel:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Model'})

        imei_number = request.POST.get('inputMobIMIE')
        if not imei_number:
            return JsonResponse({"error": 'error', 'txt_black_error': 'IMEI'})

        Mobpurchasedate = request.POST.get('inputMobpurchasedate')
        if not Mobpurchasedate:
            Mobpurchasedate = None

        MobSerialNo = request.POST.get('inputMobSerialNo')
        if not MobSerialNo:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Serial Number'})

        Mobassetid = request.POST.get('inputMobassetid')
        if not Mobassetid:
            return JsonResponse({"error": 'error', 'txt_black_error': 'Asset'})

        Mobuname = request.POST.get('inputMobuname')


        a = Mobile_records(Mobassetid=Mobassetid, MobSerialNo=MobSerialNo, imei_number=imei_number,MobMake=MobMake,MobModel=MobModel,Mobpurchasedate=Mobpurchasedate,Mobuname=Mobuname)
        a.save()

    return JsonResponse({'success': 'success', 'sys': 'sys_name'})

def Asset_location_details(request):
    location_name = location_details.objects.all()
    print(location_name)
    return render(request, 'your_app/item_dropdown.html', {'location_name': location_name})
