from django import forms

from categories.models import Category
from .models import Product, ProductImage
from django.utils.translation import gettext_lazy as _


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label=_("Категорія"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=255,
        label=_("Назва продукту"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        label=_("Опис продукту"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label=_("Ціна"),
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Product
        fields = ["category", "name", "description", "price"]

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        label=_("Зображення продукту"),
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    priority = forms.IntegerField(
        label=_("Пріоритет зображения"),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text=_("Чим менше число, тим вище пріоритет зображения.")
    )
    class Meta:
        model = ProductImage
        fields = ["image", "priority"]   # або ["image", "is_main"] якщо ти вибрав boolean