from django.db import models
from videos.models import Video, Comment
from accounts.models import User

# Create your models here.


class SubscriptionPlan(models.Model):
    NAMES_CHOICES = [
        ("B", "Basic"),
        ("P", "Pro"),
        ("A", "Annual"),
    ]
    name = models.CharField(max_length=10, choices=NAMES_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    def __repr__(self):
        return f"{self.user.username} - {self.plan.name}"
