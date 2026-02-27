from rest_framework import serializers

from .models import Laptops_records, Mobile_records, SystemInfo


class LaptopRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptops_records
        fields = '__all__'


class MobileRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile_records
        fields = '__all__'


class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
