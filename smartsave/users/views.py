from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from users.forms import MyUserUpdateForm

User = get_user_model()


class UpdateProfile(UpdateView, LoginRequiredMixin):
    model = User
    form_class = MyUserUpdateForm
    template_name = "users/user_update_form.html"
    success_url = reverse_lazy("dashboard:dashboard")

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs["pk"])
