from django.contrib.auth import views as d_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", d_views.LoginView.as_view(), name="login"),
    path("logout/", d_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", d_views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        d_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", d_views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        d_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        d_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        d_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("register/", views.register, name="user_register"),
    path("signup/", views.signup_page),
    path("profile/", views.profile),
    path("profile/change/", views.profile_change),
]
