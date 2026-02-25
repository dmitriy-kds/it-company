from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "email",
        )


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
