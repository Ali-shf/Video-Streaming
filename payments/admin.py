from django.contrib import admin
from payments.models import Transaction

# Register your models here.

@admin.register(Transaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_status', 'created_at')
    search_fields = ('user__username', 'payment_status')
    list_filter = ('payment_status', )
