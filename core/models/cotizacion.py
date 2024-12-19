from django.db import models


class Cotizacion(models.Model):
    produccion = models.ForeignKey('core.Produccion', on_delete=models.CASCADE)
    cliente = models.ForeignKey('core.Cliente', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    selection_paramenters = models.JSONField()