from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from task_manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email",
        )


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "status",
            "priority",
            "task_type",
            "assignees",
        ]

    def clean_deadline(self):
        date = self.cleaned_data["deadline"]
        if date.weekday() == 6:
            raise forms.ValidationError(
                "We don't work on Sundays!"
            )
        return date


class WorkerUpdateForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "position",
            "email"
        ]


class TaskNameDescriptionSearchForm(forms.Form):
    name_or_description = forms.CharField(max_length=50, required=False, label="")


class WorkerFirstLastNameSearchForm(forms.Form):
    first_or_last_name = forms.CharField(max_length=50, required=False, label="")
