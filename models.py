from django.db import models

# Create your models here.

class Laptops_info(models.Model):
    inputLapassetid = models.CharField(max_length=200,blank=False, null=True)
    inputLapSerialNo = models.CharField(max_length=200,blank=False, null=True)
    inputLapMake = models.CharField(max_length=200,blank=False, null=True)
    inputLapModel = models.CharField(max_length=200,blank=False, null=True)
    inputLapRAM = models.CharField(max_length=200,blank=False, null=True)
    inputLapHDD = models.CharField(max_length=200,blank=False, null=True)
    inputLapProcessor = models.CharField(max_length=200,blank=False, null=True)
    #inputLapdate = models.DateField(max_length=200)
    inputLappurchasedate = models.DateField(max_length=200,blank=False, null=True)
    inputLapuname = models.CharField(max_length=200,blank=False, null=True)


class Laptops_records(models.Model):
    Lapassetid = models.CharField(max_length=200,blank=False, null=True)
    LapSerialNo = models.CharField(max_length=200,blank=False, null=True)
    LapMake = models.CharField(max_length=200,blank=False, null=True)
    LapModel = models.CharField(max_length=200,blank=False, null=True)
    LapRAM = models.CharField(max_length=200,blank=False, null=True)
    LapHDD = models.CharField(max_length=200,blank=False, null=True)
    LapProcessor = models.CharField(max_length=200,blank=False, null=True)
    #inputLapdate = models.DateField(max_length=200)
    Lappurchasedate = models.DateField(blank=False, null=True,default="")
    Lapuname = models.CharField(max_length=200,blank=False, null=True)


class Mobile_records(models.Model):
    Mobassetid = models.CharField(max_length=200,blank=False, null=True)
    MobSerialNo = models.CharField(max_length=200, blank=False, null=True)
    imei_number  = models.CharField(max_length=200,blank=False, null=True)
    MobMake = models.CharField(max_length=200,blank=False, null=True)
    MobModel = models.CharField(max_length=200,blank=False, null=True)
    Mobpurchasedate = models.DateField(blank=False, null=True)
    Mobuname = models.CharField(max_length=200, blank=False, null=True)

class location_details(models.Model):
    location_name = models.CharField(max_length=200,blank=False, null=True)
    location_name_val = models.CharField(max_length=200, blank=False, null=True)

class Lapmake_details(models.Model):
    LapMake = models.CharField(max_length=200,blank=False, null=True)

class Mobmake_details(models.Model):
    MobMake = models.CharField(max_length=200,blank=False, null=True)
