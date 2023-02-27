"""XingCheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from main import views
from django.views.static import serve
from XingCheng import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/',views.home,),
    path('crawler/', include('crawler.urls')),
    path('accounts/', include('main.urls')),
    path('login/', views.userlogin),
    path('logout/', views.userlogout),
    path('register/', views.register),
    path('loginpage/', views.login_page),
    path('signuppage/', views.signup_page),
    path('poll/', include('poll.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', RedirectView.as_view(url='accounts/login', permanent=False)),
]
