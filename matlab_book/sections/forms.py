from django.forms import ModelForm, CharField
from django.core.validators import validate_slug
from .models import Sections


class SectionForm(ModelForm):
    slug = CharField(validators=[validate_slug])

    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Sections
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("title", "slug", "number_lesson")
        # fields = "__all__"
