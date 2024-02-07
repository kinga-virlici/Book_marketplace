from django.db import models
from django.conf import settings
from .product import Product
from .user import CustomUser


class OrderItem(models.Model): # clasa cu ajutorul careia definim caracteristicile si comportamentul pt unul sau mai multe produse dintr-o comanda
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self): # acesta metota ne retuneaza cantitatea totala a unui produs
        return self.quantity * self.product.price

    def get_final_price(self): # acesta metota ne retuneaza valoarea totala a unui produs dintr-o comanda
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    # quantity = models.PositiveIntegerField()
    # item_price = models.DecimalField(max_digits=10, decimal_places=2)
    # total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def get_total(self):  # acesta metota ne retuneaza valoarea totala a comenzii
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

