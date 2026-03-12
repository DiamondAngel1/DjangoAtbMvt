from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, 
        label=_('Ім\'я'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150, 
        label=_('Прізвище'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        label=_('Електронна пошта'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        max_length=150,
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=150,
        label=_('Підтвердження пароля'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label=_('Фотографія профілю'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', "image_small")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Така електронна адреса вже використовується.")
        return email
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     user.username = self.cleaned_data["email"]  # Використовуємо email як username
    #     if self.cleaned_data.get('image'):
    #         user.image_small = self.cleaned_data['image']
    #     if commit:
    #         user.save()
    #     return user
    