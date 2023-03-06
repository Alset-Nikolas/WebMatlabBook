from django.forms import ModelForm, CharField, ImageField, Form, FileField
from django.core.validators import validate_slug
from .models import StatisticsUser


class SectionTaskForm(ModelForm):
    class Meta:
        model = StatisticsUser
        fields = "__all__"
