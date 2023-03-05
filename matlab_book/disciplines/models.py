from django.db import models
from django.urls import reverse

# Create your models here.
class Disciplines(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "disciplines"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("disciplines:disciplines_list")
