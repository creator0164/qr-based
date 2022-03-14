from rest_framework.serializers import ModelSerializer
from account.models import User


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
