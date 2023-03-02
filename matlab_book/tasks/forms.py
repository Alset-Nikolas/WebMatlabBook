from django.forms import ModelForm, CharField, ImageField, Form, FileField
from django.core.validators import validate_slug
from .models import SectionTasks


class SectionTaskForm(ModelForm):
    slug = CharField(validators=[validate_slug])

    class Meta:
        model = SectionTasks
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SectionTaskForm, self).__init__(*args, **kwargs)
        if "image" in self.fields:
            self.fields["image"].required = False
        if "path_script" in self.fields:
            self.fields["path_script"].required = False
        if "path_test" in self.fields:
            self.fields["path_test"].required = False


class CheckMatlabFileForm(Form):
    file = FileField()
