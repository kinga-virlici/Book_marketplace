from django.db import models
from django.conf import settings


class Product(models.Model): # clasa cu ajutorul careia definim caracteristicile unui produs
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    quantity = models.IntegerField()
    book_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


