from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from core import views

router = routers.DefaultRouter()

router.register(r'company', views.CompanyView)
router.register(r'broker', views.BrokerView)
router.register(r'product', views.ProductView)
router.register(r'product_company', views.ProductCompanyView)
router.register(r'cotization', views.CotizacionView)
router.register(r'cobranza', views.CobranzaView)
router.register(r'dues', views.DuesView)
router.register(r'produccion', views.ProduccionView)
router.register(r'cliente', views.ClienteView)
router.register(r'cliente_produccion', views.AssociationProductionClienteView)

urlpatterns = [
    path("", include(router.urls)),
]
