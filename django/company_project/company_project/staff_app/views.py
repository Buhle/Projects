from uuid import uuid1
from rest_framework import status
from rest_framework import viewsets
from staff_app.models import Staff
from company_app.models import Companies
from staff_app.serializers import StaffSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def retrieve_staff_details(request):
    """Get staff details """
    if request.method == 'GET':
        staff = Staff.objects.filter(staff_id=id).allow_filtering()
        serializer = StaffSerializer(staff, many=False)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateStaffViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            staff = Staff()
            staff.staff_id = uuid1()
            staff.company_id = serializer.data['company_id']

            # Check company id exist
            item = Companies.objects.filter(company_id=staff.company_id).allow_filtering()
            number = item.count()

            if number == 0:
                # Save to database
                staff.save()

                serializer = StaffSerializer(staff)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                # Return error mesage
                return Response({'errorMessage': 'Company id does not exist.'},
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveStaffMembersViewSet(viewsets.ModelViewSet):
    """Get all staff members for specific company"""
    def retrieve(self, request, id=None, **kwargs):
        staff = Staff.objects.filter(object_id=id).allow_filtering()
        if len(staff) > 0:
            serializer = StaffSerializer(staff, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'errorMessage': 'Staff for company {} does not found'.format(id)}, status.HTTP_200_OK)


class RetrieveStaffDetailsViewSet(viewsets.ModelViewSet):
    """Get staff details """
    def retrieve(self, request, id=None, **kwargs):
        staff = Staff.objects.filter(object_id=id).allow_filtering()
        if len(staff) > 0:
            staff = staff[0]
            serializer = StaffSerializer(staff, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'errorMessage': 'Staff not found'}, status.HTTP_200_OK)
