from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from .models import Profile, Follow
from .forms import UserRegisterForm, ProfileRegisterForm

from book.models import UserBook


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

@require_POST
def follow(request: HttpRequest):

    action = request.POST.get('action')
    profile_id = request.POST.get('profile_id')

    if action and profile_id:
        try:
            profile_to = Profile.objects.get(id=profile_id)
            profile_from = Profile.objects.get(user_id=request.user.pk)

        except (Profile.DoesNotExist, Profile.MultipleObjectsReturned):
            return JsonResponse({'status': 'error', 'detail': 'Profile doesn\'t exist or multiple objects was returned'}, status=500)

        if action == 'follow':
            try:
                Follow.objects.create(user_from=profile_from, user_to=profile_to)
            except BaseException:
                return JsonResponse({'status': 'error', 'detail': 'This relationship already exists'}, status=400)
        elif action == 'unfollow':
            Follow.objects.filter(user_from=profile_from, user_to=profile_to).delete()
        else:
            return JsonResponse({'status': 'error', 'detail': 'Incorrect action'}, status=400)
            
        return JsonResponse({'status': 'ok'}, status=203)

    return JsonResponse({'status': 'error', 'detail': 'Action or id isn\'t provided'}, status=400)