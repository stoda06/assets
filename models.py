from django.db import models


class Laptops_records(models.Model):
    Lapassetid = models.CharField(max_length=200, blank=False)
    LapSerialNo = models.CharField(max_length=200, blank=False)
    LapMake = models.CharField(max_length=200, blank=False)
    LapModel = models.CharField(max_length=200, blank=False)
    LapRAM = models.CharField(max_length=200, blank=False)
    LapHDD = models.CharField(max_length=200, blank=False)
    LapProcessor = models.CharField(max_length=200, blank=False)
    Lappurchasedate = models.DateField(blank=True, null=True)
    Lapuname = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        app_label = 'assets'


class Mobile_records(models.Model):
    Mobassetid = models.CharField(max_length=200, blank=False)
    MobSerialNo = models.CharField(max_length=200, blank=False)
    imei_number = models.CharField(max_length=200, blank=False)
    MobMake = models.CharField(max_length=200, blank=False)
    MobModel = models.CharField(max_length=200, blank=False)
    Mobpurchasedate = models.DateField(blank=True, null=True)
    Mobuname = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        app_label = 'assets'


class location_details(models.Model):
    location_name = models.CharField(max_length=200, blank=False)
    location_name_val = models.CharField(max_length=200, blank=False)

    class Meta:
        app_label = 'assets'


class Lapmake_details(models.Model):
    LapMake = models.CharField(max_length=200, blank=False)

    class Meta:
        app_label = 'assets'


class Mobmake_details(models.Model):
    MobMake = models.CharField(max_length=200, blank=False)

    class Meta:
        app_label = 'assets'


class SystemInfo(models.Model):
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    memory = models.CharField(max_length=50)
    disk_size = models.CharField(max_length=50)
    Username = models.CharField(max_length=255, blank=True, default="")
    Location_name = models.CharField(max_length=255, blank=True, default="")
    system_name = models.CharField(max_length=255, blank=True, default="")
    asset_id = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'assets'

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.serial_number})"
