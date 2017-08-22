from rest_framework import serializers


class StaffSerializer(serializers.Serializer):
    company_id = serializers.UUIDField(required=True)
    staff_id = serializers.UUIDField(read_only=True)
    firstname = serializers.CharField(required=True, max_length=255)
    lastname = serializers.CharField(required=True, max_length=255)
    address = serializers.CharField(max_length=255)
    documents = serializers.ListField(child=serializers.FileField(allow_empty_file=True,
                                                                  use_url=False, required=False))
    created_at = serializers.DateTimeField(read_only=True)
