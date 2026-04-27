from django.db import models

# Create your models here.
class Book(models.Model):

    class Covers(models.TextChoices):
        HARD = 'HARD'
        SOFT = 'SOFT'


    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(
        max_length=10,
        choices=Covers.choices,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)
