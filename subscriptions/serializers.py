from rest_framework import serializers
from .models import SubscriptionPlan, Subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        source='plan', queryset=SubscriptionPlan.objects.all(), write_only=True
    )

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'plan',
            'plan_id',
            'start_date',
            'end_date',
            'is_active',
        ]
