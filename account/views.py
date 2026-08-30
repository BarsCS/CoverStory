from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Profile
from .forms import UserRegisterForm, ProfileRegisterForm

from book.models import UserBook, Book


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


def profile(request: HttpRequest, username):

    profile = get_object_or_404(Profile, user__username = username)

    user_books = UserBook.objects.filter(user=request.user).select_related('book', 'user')

    return render(
        request,
        'profiles/profile.html',
        {
            'profile': profile,
            'user_books': user_books
        }
    )