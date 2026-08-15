from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Profile
from .forms import UserRegisterForm, ProfileRegisterForm


def register(request: HttpRequest):

    if request.method == 'POST':

        user_form = UserRegisterForm(request.POST)
        profile_form =  ProfileRegisterForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user: User = user_form.save(commit=False)

            user.set_password(user_form.cleaned_data['password2'])

            user.save()

            profile = profile_form.save(commit=False)

            profile.user = user

            print(f'Profile: {profile}')

            profile.save()

            return redirect('account:login')

    user_form = UserRegisterForm()
    profile_form =  ProfileRegisterForm()

    return render(
        request,
        'registration/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )

