from rest_framework import serializers


class CompanySerializer(serializers.Serializer):
    company_id = serializers.UUIDField(read_only=True)
    company_name = serializers.CharField(required=True, max_length=255)
    company_reg = serializers.CharField(required=True, max_length=255)
    address = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

