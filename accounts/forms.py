from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, MyUser


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_general = forms.BooleanField(required=False, label="ผู้ใช้ทั่วไป")
    is_manager = forms.BooleanField(required=False, label="ผู้จัดการ")
    is_admin = forms.BooleanField(required=False, label="ผู้ดูแลระบบ")

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', 'email', 'is_general', 'is_manager', 'is_admin',
                  'first_name', 'last_name',)
           
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
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )




# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'Username (ตัวอักษรอังกฤษ)'}
#         )
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={'class': 'form-control', 'placeholder': 'Email'}
#         )
#     )
#     first_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'ชื่อ'}
#         )
#     )
#     last_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'นามสกุล'}
#         )
#     )
#     position = forms.CharField(
#         widget=forms.TextInput(
#             attrs={'class': 'form-control', 'placeholder': 'ตำแหน่งงาน'}
#         )
#     )
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={'class': 'form-control', 'placeholder': 'รหัสผ่าน'}
#         )
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={'class': 'form-control', 'placeholder': 'รหัสผ่านยืนยัน'}
#         )
#     )

class ManagerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username (ตัวอักษรอังกฤษ)'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', )
        labels = {
            'email': 'อีเมล',
            'first_name' : 'ชื่อ',
            'last_name' : 'นามสกุล',
        }
        widgets = {
            'email' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
        }

# CHOICE = [
#     ('female', 'หญิง'),
#     ('maie','ชาย'),
# ]

class ExtendedProfileForm(forms.ModelForm):
    prefix = 'extended'

    class Meta:
        model = Profile
        fields = ('gender', 'position', 'work_group',  'phone','img' )
        labels = {
            'gender': 'เพศ',
            'work_group': 'หน่วยงาน'
        }
        widgets = {
            # 'gender': forms.RadioSelect(choices=CHOICE),
            'gender': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'position': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'work_group': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
            # 'img': forms.FileInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);',}),
            # 'img': forms.FileInput()
        }






# class ExtendedProfileForm(forms.ModelForm):
#     prefix = 'extended'

#     class Meta:
#         model = Profile
#         fields = ('gender', 'work_group', 'position', 'phone', 'img')
#         labels = {
#             'gender': 'เพศ',
#             'position' : 'ตำแหน่งงาน',
#             'work_group': 'กลุ่มงาน',
#             'phone': 'กลุ่มงาน',
#             'img' : 'รูปโปรไฟล์',
#         }
#         widgets = {
#             'gender' : forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'position': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'work_group': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control mt-2', 'style':'font-weight: bold; color: rgb(8, 0, 255);'}),
#         }