from uuid import uuid1

import datetime
from rest_framework import status
from rest_framework import viewsets
from .models import Staff
from company_app.models import Companies
from .serializers import StaffSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def staff_list_and_creation(request):
    """ List all staff, or create a new staff"""
    if request.method == 'GET':
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            staff = Staff()
            staff.staff_id = uuid1()
            staff.company_id = serializer.data['company_id']
            # staff.staff_id = serializer.data['staff_id']
            staff.firstname = serializer.data['firstname']
            staff.lastname = serializer.data['lastname']
            staff.address = serializer.data['address']
            staff.created_at = datetime.datetime.now()

            docs = []
            if 'documents' in serializer.data:
                if type(serializer.data['documents']) is list:
                    for doc in serializer.data.pop('documents'):
                        docs.append(doc)
                        pass
                        # doc = Staff.objects.create(documents=doc)
                    staff.documents = docs
                else:
                    staff.documents = serializer.data['documents']

            # Check staff id exist
            item = Companies.objects.filter(company_id=staff.company_id)
            number = item.count()

            if number > 0:
                staff.save()
                serializer = StaffSerializer(staff)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return error mesage
                return Response({'errorMessage': 'Company does not exist.'},
                                status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_staff_details(request, _id):
    """Get staff details """
    if request.method == 'GET':
        staff = Staff.objects.get(staff_id=_id)
        serializer = StaffSerializer(staff, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'DELETE':
        staff = Staff.objects.get(staff_id=_id)
        if len(staff) > 0:
            staff.delete()
            return Response({'message': 'successful deleted!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'staff not deleted!'})

# =====================================================================================================================


# =====================================================================================================================

class CreateStaffViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Staff.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            staff = Staff()
            staff.staff_id = uuid1()
            staff.staff_id = serializer.data['staff_id']
            staff.firstname = serializer.data['firstname']
            staff.lastname = serializer.data['lastname']
            staff.address = serializer.data['address']
            staff.created_at = datetime.datetime.now()

            # Check staff id exist
            item = Companies.objects.filter(staff_id=staff.staff_id)
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
    """Get all staff members for specific staff"""
    def retrieve(self, request, id=None, **kwargs):
        staff = Staff.objects.get(object_id=id)
        if len(staff) > 0:
            serializer = StaffSerializer(staff, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'errorMessage': 'Staff for staff {} does not found'.format(id)}, status.HTTP_200_OK)


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
