from django.forms import ModelForm, CharField
from django.core.validators import validate_slug
from .models import Disciplines


class DisciplineForm(ModelForm):
    slug = CharField(validators=[validate_slug])

    class Meta:
        model = Disciplines
        fields = "__all__"
