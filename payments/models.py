from django.db import models
from accounts.models import User

# Create your models here.


class Transaction(models.Model):
    PAYMENT_STATUS = [
        ('PEN', 'Pending'),
        ('SUC', 'Success'),
        ('FAIL', 'Failed'),
        ('REF', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS,
        default=PAYMENT_STATUS[0][0]
    )
    ref_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.payment_status})"
    
    def __repr__(self):
        return f"{self.user.username} - {self.amount} ({self.payment_status})"

