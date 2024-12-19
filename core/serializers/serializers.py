from rest_framework import serializers
from core.models.cotizacion import Cotizacion
from core.models.cobranza import Cobranza, Dues
from core.models.produccion import Produccion
from core.models.cliente import Cliente, Association_production_cliente
from core.models.company_broker import Company, Broker, Product, Product_company


class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'


class CobranzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobranza
        fields = '__all__'


class DuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dues
        fields = '__all__'


class ProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produccion
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class Association_production_clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association_production_cliente
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Product_companySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_company
        fields = '__all__'
