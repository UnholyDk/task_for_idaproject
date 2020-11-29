from django.db import models
from django.urls import reverse

class ImageModel(models.Model):
    name = models.CharField(max_length=240, blank=True)
    url = models.URLField(blank=True, verbose_name='Ссылка')
    image = models.ImageField(upload_to='images/', verbose_name='Файл', blank=True)
    height = models.IntegerField(verbose_name='Высота', blank=True, null=True)
    width = models.IntegerField(verbose_name='Ширина', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('image_edit', args=[str(self.id)])