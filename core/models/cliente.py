from django.db import models


class Cliente(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=100)
    person_type = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Association_production_cliente(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)