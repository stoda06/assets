from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *

from datetime import date


today = date.today()

from django.template import RequestContext

# Create your views here.

def dashboard(request):
    return render(request, 'index.html', context={})




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