from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import registerForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib import admin
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tokens import account_activation_token

#  if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             message = render_to_string('acc_active_email.html', {
#                 'user':user, 'domain':current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             # Sending activation link in terminal
#             # user.email_user(subject, message)
#             mail_subject = 'Activate your blog account.'
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration.')
#             # return render(request, 'acc_active_sent.html')


def register(request):
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            token = str(account_activation_token.make_token(person))
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            p = Profile.objects.create(
                auth_token=token,
                username=username,
                email=email,
                password=password,
                is_verified=False,
            )
            p.save()
            email = request.POST.get("email", False)
            subject = "Your account needs to be verified"
            message = f"Hi click on this link to verify your account http://127.0.0.1:8000/verify/{token}"
            email_from = "shreya.bose.in@gmail.com"
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, "register/token_send.html", {})
        else:
            return redirect("/error")
    else:
        form = registerForm()
        return render(request, "register/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.info(request, "You have been logged in")
            return redirect("/home")
        else:
            messages.info(request, "Invalid form")
    else:
        return render(request, "register/login.html", {})


@login_required(login_url="/login")
def logout_fn(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("/login")


def token_send(request, token):
    email = request.POST.get("email", False)
    subject = "Your account needs to be verified"
    message = f"Hi paste your link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_from = "shreya.bose.in@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "register/token_send.html", {})


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        profile_obj.is_verified = True
        profile_obj.save()
        user = User.objects.create(
            username=profile_obj.username, email=profile_obj.email
        )
        user.set_password(profile_obj.password)
        user.save()
        messages.info(request, "Your account has been verified")
        return redirect("/login")
    else:
        return redirect("/error")


def error_page(request):
    return render(request, "register/error.html", {})
