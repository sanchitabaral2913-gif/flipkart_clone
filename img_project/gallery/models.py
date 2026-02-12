from django.db import models

CATEGORY_CHOICES = [
    ('flower', 'Flower'),
    ('god', 'God'),
    ('goddess', 'Goddess'),
]

class Image(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

