from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'uid-input'}), required=True)
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pwd-input'}), required=True)


# django register form
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'uid-input'}), required=True)
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pwd-input'}), required=True)
    pwd_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pwd-input'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email-input'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone-input'}), required=True)


class ProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'uid-input'}), required=True)
