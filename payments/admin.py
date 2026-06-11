from django.contrib import admin
from .models import Payments


@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "payment_type",
        "borrowing_id",
        "session_url",
        "session_id",
    )
