from django.db import models


class Cobranza(models.Model):
    product = models.OneToOneField('core.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    gross_prima = models.FloatField()
    dues = models.IntegerField()
    payment_type = models.CharField(max_length=50)

class Dues(models.Model):
    cobranza = models.ForeignKey(Cobranza, on_delete=models.CASCADE , related_name='due')
    due = models.IntegerField()
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    amount = models.FloatField()
    expirantion_date = models.DateField()
    pay_date = models.DateField()