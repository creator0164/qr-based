from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from .serializers import AccountSerializer


@api_view(['GET'])
def getRoutes(request, *args, **kwargs):
    routes = [
        'GET /api',
        'GET /api/accounts/',
        'GET /api/account:id/',
    ]
    return Response(routes)


@api_view(['GET'])
def getAccounts(request, *args, **kwargs):
    accounts = User.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getAccount(request, pk, *args, **kwargs):
    account = User.objects.get(id=pk)
    serializer = AccountSerializer(account, many=False)
    return Response(serializer.data)
