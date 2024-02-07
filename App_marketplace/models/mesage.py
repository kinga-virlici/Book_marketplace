from django.db import models


class Mesaj(models.Model): #clasa cu ajutorul careia definim caracteristicile unui mesaj primit de la utilizator
    STATUS_CHOICES = [
        ('necitit', 'Necitit'),
        ('rezolvat', 'Rezolvat'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='necitit')
    receiving_date = models.DateTimeField(auto_now_add=True)