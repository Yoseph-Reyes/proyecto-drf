from django.contrib import admin
from core.models.cotizacion import Cotizacion
from core.models.cobranza import Cobranza, Dues
from core.models.produccion import Produccion
from core.models.cliente import Cliente, Association_production_cliente
from core.models.company_broker import Company, Broker, Product, Product_company

admin.site.register(Cotizacion)
admin.site.register(Cobranza)
admin.site.register(Dues)
admin.site.register(Produccion)
admin.site.register(Cliente)
admin.site.register(Association_production_cliente)
admin.site.register(Company)
admin.site.register(Broker)
admin.site.register(Product)
admin.site.register(Product_company)
# Register your models here.
