from django.db import models

class Upload(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class UploadImage(models.Model):
    images = models.FileField(upload_to = 'images/')

    def __str__(self):
        return str(image)
