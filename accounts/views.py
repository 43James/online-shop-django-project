from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# from cart import cart
from cart.models import CartItem
# from cart.utils.cart import Cart
from dashboard.views import is_manager
from django.db.models import Q

# from cart.views import save_cart

from .forms import ExtendedProfileForm, UserRegistrationForm, UserLoginForm, ManagerLoginForm, UserProfileForm, UserEditForm
from accounts.models import MyUser, Profile
from cart.cart import Cart


@login_required
def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("Here1")
            form.save(commit=False)
            form.save()
            print("Here")
            messages.success(request, 'เพิ่มสมาชิกสำเร็จ')
            return redirect('accounts:manage_user')
        else:
            messages.error(request, 'เพิ่มสมาชิกไม่สำเร็จ')

    form = UserRegistrationForm()
    context = {'form':form,
               'title':'Create Account',}
    return render(request, 'register.html', context)



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
                return redirect('dashboard:dashboard_home')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = { 'title':'LogIn','form': form}
    return render(request, 'manager_login.html', context)


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


@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required
def edit_profile (request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST,  instance=user )
        is_new_profile = False
        
        try:
            #update
            extended_form = ExtendedProfileForm(request.POST, request.FILES, instance=user.profile)
        except:
            #create
            extended_form = ExtendedProfileForm(request.POST, request.FILES)
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
            extended_form = ExtendedProfileForm(request.POST, request.FILES)

    context = {
        'title':'Edit Profile',
        "form": form,
        "extended_form": extended_form,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def user_profile_detail(request, username):
    try:
        obj = 1
        user = MyUser.objects.get(username = username)
        profile = Profile.objects.get(user_id=user.id)

    except:
        obj = 2
        profile = 'คุณยังไม่ได้เพิ่มข้อมูลโปรไฟล์'
        
    context = {
        'user': user, 
        'profile': profile,
        'obj': obj,
        
    }
    return render(request, 'user_profile.html', context)


@login_required
def manage_user(request):
    my = MyUser.objects.all()
    
    query = request.GET.get('q')
    if query is not None:
        lookups = Q(username__icontains=query) | Q(first_name__icontains=query)
        my = MyUser.objects.filter(lookups)

    page = request.GET.get('page')
    p = Paginator(my, 8)
    try:
        my = p.page(page)
    except:
        my = p.page(1)

    return render(request, "manage_user.html",{
        "my" : my,
        'title':'Manage User',
    })

@user_passes_test(is_manager)
@login_required
def update_user(request, id):
    my = MyUser.objects.get(id = id)
    form = UserEditForm()
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = my)

        if form.is_valid():
            form.save()
            id=form.instance.id
            messages.success(request, 'แก้ไขข้อมูลสำเร็จ')
            return redirect('accounts:manage_user')
        else :
            messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
            
    return render(request, 'update_user.html', {
        'my':my,
        'form': form,
        'title' : 'แก้ไขข้อมูลสมาชิก'
    })

@login_required 
def delete_user(request, id):
    data_input = MyUser.objects
    delete_fil = data_input.filter(id=id).delete()
    data_all = MyUser.objects.all()
    messages.success(request, 'ลบสมาชิกสำเร็จ')
    return redirect('manage_user')

