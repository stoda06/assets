from django.http import JsonResponse
from django.shortcuts import render

from .models import *
import logging

logger = logging.getLogger(__name__)


from django.template import RequestContext

# Create your views here.

def dashboard(request):
    logger.debug("Entering dashboard")
    return render(request, 'index.html', context={})


def asset(request):
    logger.debug("Entering asset")

    # Your view logic here
    
    location_name = location_details.objects.all()
    LapMake = Lapmake_details.objects.all()
    MobMake = Mobmake_details.objects.all()
    user = request.user
    first_name = request.user.first_name
    last_name = request.user.last_name


    context = {'user': user,
               'first_name': first_name,
               'last_name': last_name,
               'location_name': location_name,
               'LapMake':LapMake,
               'MobMake':MobMake
               }
    logger.debug("Exiting asset")

    return render(request, 'laptop_asset.html', context)


def Laptops_data(request):
    logger.debug("Entering laptops_data")
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

        HDDType = request.POST.get('inputLapHDDType')

        print('its HDDType',HDDType)

        LapHDD = request.POST.get('inputLapHDD')
        if not LapHDD:
            return JsonResponse({"error": 'error','txt_black_error':'HDD'})

        print('its LapHDD', LapHDD)

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

        print('concatinated',LapHDD)


        a = Laptops_records(LapMake=LapMake, LapModel=LapModel, LapRAM=LapRAM,LapHDD=LapHDD,LapProcessor=LapProcessor,Lappurchasedate=Lappurchasedate,LapSerialNo=LapSerialNo,Lapassetid=Lapassetid,Lapuname=Lapuname)
        a.save()
    logger.debug("Exiting laptop_data")
    return JsonResponse({'success': 'success', 'sys': 'sys_name'})



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
