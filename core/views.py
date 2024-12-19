from django.shortcuts import render
from core.models.cotizacion import Cotizacion
from core.models.cobranza import Cobranza, Dues
from core.models.produccion import Produccion
from core.models.cliente import Cliente, Association_production_cliente
from core.models.company_broker import Company, Broker, Product, Product_company
from core.serializers.serializers import *
from rest_framework import (filters, permissions, response, serializers,decorators,
                            status, viewsets)
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    view_name = 'CompanyView'


class BrokerView(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    view_name = 'BrokerView'


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    view_name = 'ProductView'


class ProductCompanyView(viewsets.ModelViewSet):
    queryset = Product_company.objects.all()
    serializer_class = Product_companySerializer
    view_name = 'ProductCompanyView'


class CotizacionView(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer
    view_name = 'CotizacionView'


class CobranzaView(viewsets.ModelViewSet):
    queryset = Cobranza.objects.all()
    serializer_class = CobranzaSerializer
    view_name = 'CobranzaView'


class DuesView(viewsets.ModelViewSet):
    queryset = Dues.objects.all()
    serializer_class = DuesSerializer
    view_name = 'DuesView'


class ProduccionView(viewsets.ModelViewSet):
    queryset = Produccion.objects.all()
    serializer_class = ProduccionSerializer
    view_name = 'ProduccionView'


class ClienteView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    view_name = 'ClienteView'


class AssociationProductionClienteView(viewsets.ModelViewSet):
    queryset = Association_production_cliente.objects.all()
    serializer_class = Association_production_clienteSerializer
    view_name = 'AssociationProductionClienteView'
