from django.contrib import admin

from .models import *

# Register your models here.


class Laptops_recordsAdmin(admin.ModelAdmin):
    list_display = ('LapMake',
'LapModel',
'LapRAM',
'LapHDD',
'LapProcessor',
'Lappurchasedate',
'LapSerialNo',
'Lapassetid','Lapuname')



class Mobile_recordsAdmin(admin.ModelAdmin):
    list_display = ('Mobassetid','MobSerialNo','imei_number','MobMake','MobModel','Mobpurchasedate')

class location_detailsAdmin(admin.ModelAdmin):
    list_display = ('location_name','location_name_val')

class Lapmake_detailsAdmin(admin.ModelAdmin):
    list_display = ('LapMake',)

class Mobmake_detailsAdmin(admin.ModelAdmin):
    list_display = ('MobMake',)


admin.site.register(Lapmake_details, Lapmake_detailsAdmin)
admin.site.register(Mobmake_details, Mobmake_detailsAdmin)
admin.site.register(Laptops_records, Laptops_recordsAdmin)
admin.site.register(Mobile_records, Mobile_recordsAdmin)
admin.site.register(location_details, location_detailsAdmin)
#admin.site.register(make_details, make_detailsAdmin)

