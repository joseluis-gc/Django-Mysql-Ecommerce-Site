from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Order(models.Model):
    token = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Order Total Dlls')
    email_address = models.CharField(max_length=255, blank=True, verbose_name='Email')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=255, blank=True)
    billingAddress1 = models.CharField(max_length=255, blank=True)
    billingCity = models.CharField(max_length=255, blank=True)
    billingPostCode = models.CharField(max_length=255, blank=True)
    billingCountry = models.CharField(max_length=255, blank=True)
    ShippingName = models.CharField(max_length=255, blank=True)
    ShippingAddress1 = models.CharField(max_length=255, blank=True)
    ShippingCity = models.CharField(max_length=255, blank=True)
    ShippingPostCode = models.CharField(max_length=255, blank=True)
    ShippingCountry = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)


class orderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Dlls")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table= 'orderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return str(self.product)

