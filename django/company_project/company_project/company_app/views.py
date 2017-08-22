from uuid import uuid1

import datetime
from rest_framework import status
from rest_framework import viewsets
from .models import Companies
from .serializers import CompanySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def company_list_and_creation(request):
    """ List all companies, or create a new company"""
    if request.method == 'GET':
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = Companies()
            company.company_id = uuid1()
            company.company_name = serializer.data['company_name']
            company.company_reg = serializer.data['company_reg']
            company.address = serializer.data['address']
            company.created_at = datetime.datetime.now()
            # Check company id exist
            item = Companies.objects.filter(company_name=company.company_name)
            number = item.count()

            if number == 0:
                company.save()
                serializer = CompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return error mesage
                return Response({'errorMessage': 'Company with the same name exist.'},
                                status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def retrieve_company_details(request, _id):
    """Get company details """
    if request.method == 'GET':
        print('here')
        company = Companies.objects.get(company_id=_id)
        print(company)
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'DELETE':
        company = Companies.objects.filter(company_id=id)
        if len(company) > 0:
            company.delete()
            return Response({'message': 'successful deleted!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'company not deleted!'})

# ====================================================================================================================


# =====================================================================================================================
class DefaultMixin(object):
    serializer_class = CompanySerializer
    paginate_by = 10


class CreateCompanyViewSet(DefaultMixin, viewsets.ModelViewSet):
    def get_queryset(self):
        return Companies.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = Companies()
            company.company_id = uuid1()
            company.company_name = serializer.data['company_name']

            # Check company id exist
            item = Companies.objects.filter(company_name=company.company_name).allow_filtering()
            number = item.count()

            if number == 0:
                # Save to database
                company.save()

                serializer = CompanySerializer(company)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                # Return error mesage
                return Response({'errorMessage': 'Company with the same name exist.'},
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None, **kwargs):
        staff = Companies.objects.filter().allow_filtering()
        serializer = CompanySerializer(staff, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


