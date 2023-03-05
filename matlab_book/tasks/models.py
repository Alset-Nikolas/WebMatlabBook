from django.db import models
from sections.models import Sections
from django.urls import reverse

# Create your models here.
class SectionTasks(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(
        Sections,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=300)
    text = models.TextField(max_length=1500)
    image = models.ImageField(
        upload_to="tasks/img/",
        null=True,
        blank=True,
    )
    path_script = models.FileField(
        upload_to="tasks/matlab_scripts/",
        null=True,
        blank=True,
    )
    path_test = models.FileField(
        upload_to="tasks/tests/",
        null=True,
        blank=True,
    )
    complexity = models.IntegerField()
    is_laba = models.BooleanField(default=False)

    class Meta:
        db_table = "section_tasks"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sections:sections_list")
