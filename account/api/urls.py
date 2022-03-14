from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('accounts/', views.getAccounts),
    path('accounts/<str:pk>/', views.getAccount),
]
