from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import forms
from flights import models



def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required
def user_profile_view(request):
    user = request.user
    passenger = models.Passenger.objects.get(user=user)

    # Default empty forms
    first_name_form = forms.FirstNameUpdateForm(instance=user)
    last_name_form = forms.LastNameUpdateForm(instance=user)

    if request.method == 'POST':
        if 'first_name' in request.POST:
            first_name_form = forms.FirstNameUpdateForm(request.POST, instance=user)
            if first_name_form.is_valid():
                first_name_form.save()
                return redirect('users:user_profile')

        elif 'last_name' in request.POST:
            last_name_form = forms.LastNameUpdateForm(request.POST, instance=user)
            if last_name_form.is_valid():
                last_name_form.save()
                return redirect('users:user_profile')

    return render(request, 'users/user_profile.html', {
        'user': user,
        'passenger': passenger,
        'first_name_form': first_name_form,
        'last_name_form': last_name_form,
    })

def register_view(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            models.Passenger.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect('flights:index')

        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = forms.UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flights:index')
            else:
                return render(request, 'users/login.html', {
                    'form': form,
                    'error': 'Invalid username or password.'
                })
    else:
        form = forms.UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})
