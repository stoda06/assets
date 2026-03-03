import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Lapmake_details,
    Laptops_records,
    Mobile_records,
    Mobmake_details,
    SystemInfo,
    location_details,
)
from .serializers import SystemInfoSerializer

logger = logging.getLogger(__name__)


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


@login_required
def dashboard(request):
    return render(request, 'index.html', context={})


@login_required
def asset(request):
    try:
        location_name = location_details.objects.all()
        LapMake = Lapmake_details.objects.all()
        MobMake = Mobmake_details.objects.all()
        Laptop_data = Laptops_records.objects.all()
        device_data = SystemInfo.objects.all()
    except Exception:
        logger.exception("Database error loading asset data")
        return render(request, '500.html', status=500)

    user = request.user
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + ' ' + last_name

    context = {
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': full_name,
        'location_name': location_name,
        'LapMake': LapMake,
        'MobMake': MobMake,
        'Laptop_data': Laptop_data,
        'device_data': device_data,
    }
    return render(request, 'laptop_asset.html', context)


@login_required
def Laptops_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    LapMake = request.POST.get('inputLapMake')
    if not LapMake:
        return JsonResponse({"error": 'error', 'txt_black_error': 'Make'})

    LapModel = request.POST.get('inputLapModel')
    if not LapModel:
        return JsonResponse({"error": 'error', 'txt_black_error': 'Model'})

    LapRAM = request.POST.get('inputLapRAM')
    if not LapRAM:
        return JsonResponse({"error": 'error', 'txt_black_error': 'RAM'})
    try:
        ram_value = int(LapRAM)
    except (ValueError, TypeError):
        return JsonResponse({"error": 'error', 'txt_black_error': 'RAM must be a number'})
    if ram_value > 100:
        return JsonResponse({"RAM_Greater": 'RAM_Greater', 'txt_black_error': 'RAM'})
    if ram_value < 1:
        return JsonResponse({"RAM_lower": 'RAM_lower', 'txt_black_error': 'RAM'})

    HDDType = request.POST.get('inputLapHDDType')
    if not HDDType:
        return JsonResponse({"error": 'error', 'txt_black_error': 'HDD Type'})

    LapHDD = request.POST.get('inputLapHDD')
    if not LapHDD:
        return JsonResponse({"error": 'error', 'txt_black_error': 'HDD'})
    try:
        hdd_value = int(LapHDD)
    except (ValueError, TypeError):
        return JsonResponse({"error": 'error', 'txt_black_error': 'HDD must be a number'})
    if (hdd_value < 100 or hdd_value > 5000) and HDDType == 'GB':
        return JsonResponse({'HDD_ERROR': 'HDD_ERROR', 'txt_black_error': 'HDD'})
    if hdd_value > 5 and HDDType == 'TB':
        return JsonResponse({'HDD_ERROR': 'HDD_ERROR', 'txt_black_error': 'HDD'})

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

    LapHDD = LapHDD + ' ' + HDDType

    try:
        condition1 = Q(Lapassetid=Lapassetid)
        condition2 = Q(Lapuname=Lapuname)
        combined_condition = condition1 | condition2

        if Laptops_records.objects.filter(combined_condition).exists():
            return JsonResponse({'exists': 'exists'})

        Laptops_records.objects.create(
            LapMake=LapMake,
            LapModel=LapModel,
            LapRAM=LapRAM,
            LapHDD=LapHDD,
            LapProcessor=LapProcessor,
            Lappurchasedate=Lappurchasedate,
            LapSerialNo=LapSerialNo,
            Lapassetid=Lapassetid,
            Lapuname=Lapuname,
        )
    except Exception:
        logger.exception("Database error saving laptop record")
        return JsonResponse({"error": "A server error occurred"}, status=500)
    return JsonResponse({'success': 'success', 'sys': 'sys_name'})


@login_required
def Mobile_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    MobMake = request.POST.get('inputMobMake')
    if not MobMake:
        return JsonResponse({"error": 'error', 'txt_black_error': 'Make'})

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

    try:
        condition1 = Q(Mobassetid=Mobassetid)
        condition2 = Q(imei_number=imei_number)
        combined_condition = condition1 | condition2

        if Mobile_records.objects.filter(combined_condition).exists():
            return JsonResponse({'exists': 'exists'})

        Mobile_records.objects.create(
            Mobassetid=Mobassetid,
            MobSerialNo=MobSerialNo,
            imei_number=imei_number,
            MobMake=MobMake,
            MobModel=MobModel,
            Mobpurchasedate=Mobpurchasedate,
            Mobuname=Mobuname,
        )
    except Exception:
        logger.exception("Database error saving mobile record")
        return JsonResponse({"error": "A server error occurred"}, status=500)
    return JsonResponse({'success': 'success', 'sys': 'sys_name'})


@login_required
def Asset_location_details(request):
    try:
        loc_names = location_details.objects.all()
    except Exception:
        logger.exception("Database error loading location details")
        return render(request, '500.html', status=500)
    return render(request, 'your_app/item_dropdown.html', {'location_name': loc_names})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def systeminfo_create(request):
    """Accept system info from endpoints without requiring authentication."""
    # Flatten any list values to strings (WMI commands return arrays)
    data = {}
    for key, value in request.data.items():
        if isinstance(value, list):
            data[key] = ", ".join(str(v) for v in value)
        else:
            data[key] = value

    # Skip virtual machines — don't store VMware entries
    vmware_fields = ['manufacturer', 'model', 'serial_number', 'processor']
    for field in vmware_fields:
        val = data.get(field, '')
        if isinstance(val, str) and 'vmware' in val.lower():
            return Response(
                {"detail": "Rejected", "message": "Virtual machine data is not collected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    serial = data.get('serial_number')
    if serial and SystemInfo.objects.filter(serial_number=serial).exists():
        return Response(
            {"detail": "Duplicate entry", "message": "This record already exists in the database."},
            status=status.HTTP_409_CONFLICT,
        )

    serializer = SystemInfoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def delete_device(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    device_id = request.POST.get('device_id')
    if not device_id:
        return JsonResponse({"error": "Device ID is required"}, status=400)

    try:
        device = SystemInfo.objects.get(id=device_id)
        device.delete()
    except SystemInfo.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
    except Exception:
        logger.exception("Database error deleting device record")
        return JsonResponse({"error": "A server error occurred"}, status=500)
    return JsonResponse({"success": "success"})
