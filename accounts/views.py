from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import ExtendedProfileForm, UserRegistrationForm, UserLoginForm, ManagerLoginForm, UserProfileForm
from accounts.models import MyUser


# def create_manager():
#     """
#     to execute once on startup:
#     this function will call in online_shop/urls.py
#     """
#     if not MyUser.objects.filter(email="manager@example.com").first():
#         user = MyUser.objects.create_user(
#             "manager@example.com", 'shop manager' ,'managerpass1234'
#         )
#         # give this user manager role
#         user.is_manager = True
#         user.save()


def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user is not None and user.is_manager and user.is_admin:
                login(request, user)
                return redirect('dashboard:products')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = {'form': form}
    return render(request, 'manager_login.html', context)


# def user_register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             MyUser = MyUser.objects.create_user(
#                 data['username'], data['email'], data['first_name'], data['last_name'], data['position'], data['password']
#             )
#             return redirect('accounts:user_login')
#     else:
#         form = UserRegistrationForm()
#     context = {'title':'Signup', 'form':form}
#     return render(request, 'register.html', context)

def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Here1")
            form.save(commit=False)
            form.save()
            print("Here")
            messages.success(request, 'เพิ่มสมาชิกสำเร็จ')
            return redirect('accounts:user_login')
        else:
            messages.error(request, 'เพิ่มสมาชิกไม่สำเร็จ')

    form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'register.html', context)



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('shop:home_page')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


# def edit_profile(request):
#     form = UserProfileForm(request.POST, instance=request.user)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Your profile has been updated', 'success')
#         return redirect('accounts:edit_profile')
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {'title':'Edit Profile', 'form':form}
#     return render(request, 'edit_profile.html', context)


def edit_profile (request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False
        
        try:
            #update
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            #create
            extended_form = ExtendedProfileForm(request.POST)
            is_new_profile = True

        if form.is_valid() and extended_form.is_valid():
            form. save()

            if is_new_profile:
                #create
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            else:
                #update
                extended_form.save()
                messages.success(request, 'บันทึกข้อมูลสำเร็จ')
            return redirect('accounts:edit_profile')

    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()

    context = {
        'title':'Edit Profile',
        "form": form,
        "extended_form": extended_form
    }
    return render(request, 'edit_profile.html', context)