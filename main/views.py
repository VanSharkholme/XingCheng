from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import User
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = User.objects.get(username=username)
        return render(request, 'home.html', {'user': user})
    else:
        form = LoginForm()
        return render(request, 'home.html', {'login_form': form})


def userlogin(request):
    form = LoginForm()
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
    return render(request, 'home.html', {'login_form': form})


def userlogout(request):
    logout(request)
    return redirect('/')
    # pass

# django register view

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             email = form.cleaned_data['email']
#             user = User.objects.create_user(username=username, password=password, email=email)
#             user.save()
#             return HttpResponseRedirect(reverse('login'))
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'register_form': form})
#


