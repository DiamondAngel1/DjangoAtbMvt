from django.db import models
from slugify import slugify

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    slug = models.SlugField(
        max_length=225,
        blank=True
    )
    # image= ResizedImageField(
    #     size=[800, 600],
    #     quality=90,
    #     force_format='WEBP',
    #     upload_to=upload_images,
    #     null=True,
    #     blank=True
    # )
    image = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    