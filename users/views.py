from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.forms import UserLoginForm, UserProfileForm
from django.contrib import auth
from products.models import Basket
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def register(requests):
    return render(requests, 'users/register.html')


@login_required()
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
    total_quantity = 0
    total_sum = 0
    baskets = Basket.objects.filter(user=user)
    for basket in baskets:
        total_quantity += basket.quantity
        total_sum += basket.sum()

    context = {'form': form,
               'baskets': Basket.objects.filter(user=user),
               'total_quantity': total_quantity,
               'total_sum': total_sum,
    }
    return render(request, 'users/profile.html', context)
