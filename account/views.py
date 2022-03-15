from multiprocessing import context
from account.forms import UserAuthenticationForm, RegistrationForm
from account.models import User

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def index(request, *args, **kwargs):
    context = {}
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login-view')

    context['user'] = user
    return render(request, 'base/index.html', context)


def login_view(request, *args, **kwargs):
    context = {}

    if request.user.is_authenticated:
        return redirect('home')

    destination = get_redirect_if_exists(request)

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(
                username=username, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect('home')

    else:
        form = UserAuthenticationForm()

    context['login_form'] = form
    return render(request, 'base/login.html', context)


def register_view(request, user_http=False, *args, **kwargs):
    context = {}
    user = request.user
    current_site = get_current_site(request)
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = request.POST['email']
            user_email = User.objects.get(email=email)
            subject = 'Email Confirmation From QR'
            message = render_to_string('base/email_send/email_send.html', {
                'protocol': 'https' if user_http else 'http',
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_email.pk)),
                'token': default_token_generator.make_token(user_email),
                'email': email,
            })
            email_send = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_send.fail_silently = False
            email_send.send()
            messages.success(
                request, 'Check your email to activate your account')
            return redirect('login-view')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'base/register.html', context)


def logout_view(request, *args, **kwargs):
    logout(request, )
    return redirect('login-view')


def forgot_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'base/forgot-password.html')


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def email_activation(request, uidb64, token):
    context = {}
    try:
        t1 = 'not'
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            t1 = 'OK'
            user.is_active = True
            user.save()
    except User.DoesNotExist:
        return HttpResponse('This activation link already used.')
    except:
        return HttpResponse('Activation fail please try again later.')
    context['user'] = user
    return render(request, 'base/email_send/email_activation_success.html', context)


def setting_view(request, *args, **kwargs):
    context = {}

    if not request.user.is_authenticated:
        return redirect('login-view')
    return render(request, 'base/setting.html', context)


def profile_view(request, *args, **kwargs):
    context = {}
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if not request.user.is_authenticated:
        return redirect('login-view')

    context['qr'] = user.qr_code.url
    return render(request, 'base/profile.html', context)


def error_404(request, exception):
    return render(request, 'base/error_404.html')
