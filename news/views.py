from random import randint
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def registraion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        code = str(randint(100000, 999999))
        ConfEmail.objects.create(user=user, code=code)
        send_mail(
            'Подтверждение почты',
            f'Твой код: {code}',
            'norep1y@softc1ub.tj',
            [user.email]
        )
        return redirect('confirm_email')

    return render(request, 'registration.html')


def confirm_email(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        user = User.objects.filter(username=username).first()

        if ConfEmail.objects.filter(user=user, code=code).first():
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile')

        return redirect('confirm_email')

    return render(request, 'confirm_email.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')
    return render(request, 'login.html')


@login_required
def show_profile(request):
    news = News.objects.all()
    return render(request, 'profile.html', {'tasks': news})


@login_required
def admin_panel(request):
    news = News.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'admin_panel.html', {'news': news, 'categories': categories})


@login_required
def create_news(request):
    if request.user.groups.filter(name='Users').first():
        if request.method == 'POST':
            News.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                category_id=request.POST.get('category'),
                image=request.FILES.get('image'),
                user=request.user
            )
    else:
        return render(request, 'error.html')
    return redirect('admin_panel')


@login_required
def update_news(request, pk):
    if request.user.groups.filter(name='Users').first():
        if request.method == 'POST':
            news = get_object_or_404(News, id=pk, user=request.user)
            news.title = request.POST.get('title')
            news.description = request.POST.get('description')
            news.category_id = request.POST.get('category')
            if request.FILES.get('image'):
                news.image = request.FILES.get('image')
            news.save()
    else:
        return render(request, 'error.html')
    return redirect('admin_panel')


@login_required
def delete_news(request, pk):
    if request.user.groups.filter(name='Users'):
        if request.method == 'POST':
            news = get_object_or_404(News, id=pk, user=request.user)
            news.delete()
    else:
        return render(request, 'error.html')
    return redirect('admin_panel')


@login_required
def search_news(request):
    title = request.GET.get('title')
    news = News.objects.filter(title__icontains=title)
    return render(request, 'profile.html', {'tasks': news, 'title': title})
