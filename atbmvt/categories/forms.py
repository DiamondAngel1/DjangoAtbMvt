from django import forms
from .models import Category
from django.utils.translation import gettext_lazy as _

class CategoryCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label=_('Назва категорії'),
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': _('Введіть назву категорії')})
    )
    description = forms.CharField(
        required=False,
        label=_('Опис категорії'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Опишіть категорію'),
            'rows': 4
        })
    )
    slug = forms.SlugField(
        max_length=225,
        required=False,
        label=_('Slug категорії'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введіть slug категорії')
        })
    )
    image = forms.ImageField(
        required=False,
        label=_('Зображення категорії'),
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'slug']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 4:
            raise forms.ValidationError("Назва має бути довшою за 4 символи.")
        return name
