from django.urls import path
from . import views

urlpatterns = [
    path("logout/", views.logout_fn, name="logout"),
    path("register/", views.register, name="register"),
    path("token_send/", views.token_send, name="token_send"),
    path("verify/<auth_token>", views.verify, name="verify"),
    path("error", views.error_page, name="error"),
]
