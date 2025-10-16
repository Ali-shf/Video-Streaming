from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'payment_status', 'ref_code', 'created_at']
