from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, PasswordResetCount, LoginCount
from django.contrib import messages
from django.contrib.auth.views import PasswordResetCompleteView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:

        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})


class MyPasswordResetCompleteView(PasswordResetCompleteView):

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)  # DICT
        try:
            context['password_reset_count'] = PasswordResetCount.objects.first().count

        except ObjectDoesNotExist:
            pass

        return context

    def get(self, request, *args, **kwargs):
        count_object, created = PasswordResetCount.objects.get_or_create(pk=1)
        count_object.count += 1
        count_object.save()
        return super().get(request, *args, **kwargs)


class CountLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        login_count, created = LoginCount.objects.get_or_create(id=1)
        login_count.count += 1
        login_count.save()

        return response


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',
                            {'section': 'people',
                            'users': users})
@login_required
def user_detail(request, username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request,'account/user/detail.html',
                            {'section': 'people',
                            'user': user})