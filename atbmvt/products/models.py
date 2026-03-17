from django.db import models
import slugify
from categories.models import Category

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        max_length=225,
        blank=True,
        unique=True,
        null=True
    )
    description = models.TextField(
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return f"{self.name} - {self.category.name}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True
    )
    image = models.ImageField(upload_to='product_images/')
    priority = models.PositiveIntegerField(default=0, help_text="Чим менше число, тим вище пріоритет зображення.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'created_at']
    
    def save(self, *args, **kwargs):
        if self.priority == 0:
            max_priority = ProductImage.objects.filter(product=self.product).aggregate(models.Max('priority'))['priority__max']
            self.priority = (max_priority or 0) + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage = self.image.storage
        path = self.image.path
        super().delete(*args, **kwargs)
        if storage.exists(path):
            storage.delete(path)
            
    def __str__(self):
        return f"Зображення для {self.product.name} (Пріоритет: {self.priority})"
    