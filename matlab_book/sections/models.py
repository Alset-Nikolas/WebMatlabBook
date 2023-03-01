from django.db import models
from django.urls import reverse

# Create your models here.
class Sections(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    number_lesson = models.IntegerField()

    class Meta:
        db_table = "sections"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sections:sections_list")
