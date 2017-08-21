from uuid import uuid1
from rest_framework import status
from rest_framework import viewsets
from company_app.models import Companies
from company_app.serializers import CompanySerializer
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
            company.company_name = serializer.data['company_name']

            # Check company id exist
            item = Companies.objects.filter(company_id=company.company_name).allow_filtering()
            number = item.count()

            if number == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return error mesage
                return Response({'errorMessage': 'Company with the same name exist.'},
                                status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_company_details(request):
    """Get company details """
    if request.method == 'GET':
        company = Companies.objects.filter(company_id=id).allow_filtering()
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateCompanyViewSet(viewsets.ModelViewSet):
    def get(self, request):
        staff = Companies.objects.filter().allow_filtering()
        serializer = CompanySerializer(staff, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = Companies()
            company.company_id = uuid1()
            company.company_name = serializer.data['company_name']

            # Check company id exist
            item = Companies.objects.filter(company_id=company.company_name).allow_filtering()
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


