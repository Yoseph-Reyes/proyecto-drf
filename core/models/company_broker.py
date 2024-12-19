from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    limist = models.JSONField()

class Product_company(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

class Broker(models.Model):
    name = models.CharField(max_length=100)
    enabled_products = models.ManyToManyField(Product)


