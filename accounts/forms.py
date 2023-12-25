from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, MyUser



class RegistrationForm(UserCreationForm):
    perfix = forms.ChoiceField(choices=MyUser.PREFIX_CHOICES, label='คำนำหน้า', widget=forms.Select(attrs={'class': 'form-control mt-2', 'style': 'font-weight: bold; color: rgb(8, 0, 255);'}))
    email = forms.EmailField(required=True)
    is_general = forms.BooleanField(required=False, label="ผู้ใช้ทั่วไป")
    is_manager = forms.BooleanField(required=False, label="ผู้จัดการระบบ")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")
    
    class Meta:
        model = MyUser
        fields = ['perfix', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_general', 'is_manager', 'is_admin']

    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'position', 'work_group', 'phone']


class UserEditForm(UserCreationForm):
    perfix = forms.ChoiceField(choices=MyUser.PREFIX_CHOICES, label='คำนำหน้า', widget=forms.Select(attrs={'class': 'form-control mt-2', 'style': 'font-weight: bold; color: rgb(8, 0, 255);'}))
    email = forms.EmailField(required=True)
    is_general = forms.BooleanField(required=False, label="ผู้ใช้ทั่วไป")
    is_manager = forms.BooleanField(required=False, label="ผู้จัดการระบบ")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'perfix', 'first_name', 'last_name', 
                  'is_general', 'is_manager', 'is_admin',)






class UserRegistrationForm(UserCreationForm):
    perfix = forms.ChoiceField(choices=MyUser.PREFIX_CHOICES, label='คำนำหน้า', widget=forms.Select(attrs={'class': 'form-control mt-2', 'style': 'font-weight: bold; color: rgb(8, 0, 255);'}))
    email = forms.EmailField(required=True)
    is_general = forms.BooleanField(required=False, label="ผู้ใช้ทั่วไป")
    is_manager = forms.BooleanField(required=False, label="ผู้จัดการระบบ")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'perfix', 'first_name', 'last_name', 
                  'is_general', 'is_manager', 'is_admin')
           
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.is_general = True
        user.is_manager = False
        user.is_admin = False

        if commit:
            user.save()
        return user



        
           
class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Password'}
        )
    )


class ManagerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
    )



# class UserProfileForm(forms.ModelForm):

#     perfix = forms.ChoiceField(choices=MyUser.PREFIX_CHOICES, label='คำนำหน้า', widget=forms.Select(attrs={'class': 'form-control mt-2', 'style': 'font-weight: bold; color: rgb(8, 0, 255);'}))

#     class Meta:
#         model = MyUser
#         fields = ('username', 'email', 'perfix', 'first_name', 'last_name', )
#         labels = {
#             'username' : 'Username',
#             'email': 'อีเมล',
#             'perfix':'คำนำหน้า',
#             'first_name' : 'ชื่อ',
#             'last_name' : 'นามสกุล',
#         }
#         widgets = {
#             'username' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'email' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'perfix' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'first_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'last_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#         }

# class ExtendedProfileForm(forms.ModelForm):
#     prefix = 'extended'

#     class Meta:
#         model = Profile
#         fields = ('gender', 'position', 'work_group', 'phone', 'img' )
#         labels = {
#             'gender': 'เพศ',
#             'position' : 'ตำแหน่ง',
#             'work_group': 'กลุ่มงาน',
#             'phone' : 'โทรศัพท์',
#             'img' : 'รูปโปรไฟล์'
#         }
#         widgets = {
#             'gender': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'position': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'work_group': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             # 'img': forms.FileInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);',}),
#             # 'img': forms.FileInput()
#         }

class UserProfileForm(forms.ModelForm):
    perfix = forms.ChoiceField(choices=MyUser.PREFIX_CHOICES, label='คำนำหน้า', widget=forms.Select(attrs={'class': 'form-control mt-2', 'style': 'font-weight: bold; color: rgb(8, 0, 255);'}))

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'perfix', 'first_name', 'last_name', )
        labels = {
            'username' : 'Username',
            'email': 'อีเมล',
            'perfix':'คำนำหน้า',
            'first_name' : 'ชื่อ',
            'last_name' : 'นามสกุล',
        }
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'email' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'perfix' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
        }

class ExtendedProfileForm(forms.ModelForm):
    gender = forms.CharField(label='เพศ', widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}))
    position = forms.CharField(label='ตำแหน่ง', widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}))
    work_group = forms.CharField(label='กลุ่มงาน', widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}))
    phone = forms.CharField(label='โทรศัพท์', widget=forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}))
    img = forms.ImageField(label='รูปโปรไฟล์', required=False, widget=forms.FileInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}))

    class Meta:
        model = Profile
        fields = ('gender', 'position', 'work_group', 'phone', 'img' )
        labels = {
            'gender': 'เพศ',
            'position' : 'ตำแหน่ง',
            'work_group': 'กลุ่มงาน',
            'phone' : 'โทรศัพท์',
            'img' : 'รูปโปรไฟล์'
        }