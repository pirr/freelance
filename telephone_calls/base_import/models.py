from django.db import models

# Create your models here.


class Base(models.Model):
    basefile = models.FileField(upload_to='bases/%Y/%m/%d')
