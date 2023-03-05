from django.db import models
from django.urls import reverse
from disciplines.models import Disciplines

# Create your models here.
class Sections(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    number_lesson = models.IntegerField()
    discipline = models.ForeignKey(
        Disciplines,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    class Meta:
        db_table = "sections"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "sections:sections_list", slug_discipline=self.discipline.slug
        )
