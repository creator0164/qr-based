from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('register/', views.register_view, name='register-view'),
    path('qr/profile/', views.profile_view, name='profile-view'),
    path('qr/setting/', views.setting_view, name='setting-view'),

    path('email_send/<uidb64>/<token>/',
         views.email_activation, name='email_send'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'),
         name='reset_password'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_change_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),

]
