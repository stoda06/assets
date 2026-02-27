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

    def to_internal_value(self, data):
        """Flatten any list values to comma-separated strings before field validation.

        Windows WMI commands (e.g. Win32_Processor) can return arrays,
        which arrive as JSON lists instead of plain strings.
        """
        data = data.copy()
        for field_name, value in data.items():
            if isinstance(value, list):
                data[field_name] = ", ".join(str(v) for v in value)
        return super().to_internal_value(data)
