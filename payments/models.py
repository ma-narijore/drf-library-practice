from borrowings.models import Borrowing
from django.db import models


class Payments(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'


    class PaymentType(models.TextChoices):
        PAYMENT = 'payment', 'Payment'
        FINE = 'fine', 'Fine'


    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
    )

    payment_type = models.CharField(
        max_length=10,
        choices=PaymentType.choices,
    )

    borrowing_id = models.ForeignKey(
        Borrowing,
        on_delete=models.CASCADE,
        related_name='payments',
    )

    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
