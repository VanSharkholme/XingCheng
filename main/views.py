import sys

import django.contrib.auth.models
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import os
from .forms import LoginForm, RegisterForm
from .models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.get(username=username)
        return render(request, 'home.html', {'user': user})
    else:
        return render(request, 'home.html', )


def login_page(request):
    return render(request, 'registration/login.html', {'btn': 'login'})


def signup_page(request):
    return render(request, 'registration/login.html', {'btn': 'signup'})


def userlogin(request):
    lg_form = LoginForm()
    rg_form = RegisterForm()
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'err_message': 'login failed'}
            return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', {'login_form': lg_form, 'register_form': rg_form})


def userlogout(request):
    logout(request)
    return redirect('/')
    # pass


# django register view

def register(request):
    if request.method == 'POST':
        rg_form = RegisterForm(request.POST)
        if rg_form.is_valid():
            username = rg_form.cleaned_data['username']
            password = rg_form.cleaned_data['pwd']
            email = rg_form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        lg_form = LoginForm()
        rg_form = RegisterForm()
    return render(request, 'home.html', {'login_form': lg_form, 'register_form': rg_form})


def profile(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.get(username=username)
        context['user'] = user
        try:
            context['avatar'] = user.profile.Avatar.url
            return render(request, 'registration/profile.html', context)
        except ObjectDoesNotExist:
            return render(request, 'registration/profile.html', context)
            pass
    else:
        return redirect('/')


def profile_change(request):
    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    if request.method == 'POST':
        print(request.POST)
        # print(request.FILES)
        username = request.user.get_username()
        user = User.objects.get(username=username)

        if 'avatar' in request.FILES:
            new_avatar = request.FILES['avatar']
            avatar_path = 'avatar/' + user.username + '.png'
            p = 'media/' + avatar_path
            with open(p, 'wb+') as avatar:
                avatar.write(new_avatar.read())
                pass
            user.profile.Avatar = avatar_path
            # print(user.profile.Avatar)

        if 'username' in request.POST:
            new_username = request.POST['username']
            user.username = new_username

        if 'email' in request.POST:
            new_email = request.POST['email']
            user.email = new_email

        if 'intro' in request.POST:
            new_intro = request.POST['intro']
            user.profile.Intro = new_intro

        user.profile.save()
        user.save()
        return redirect('/accounts/profile')
    pass
