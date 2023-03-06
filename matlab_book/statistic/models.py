from django.db import models
from tasks.models import SectionTasks
from django.urls import reverse

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class StatisticsUser(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        SectionTasks,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    flag = models.BooleanField(default=False)

    class Meta:
        db_table = "statistics_user"

    def get_absolute_url(self):
        return reverse(
            "statistics:statistics_list",
            kwargs={"discipline_slug": self.task.section.discipline.slug},
        )
