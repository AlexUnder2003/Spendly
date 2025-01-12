from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


from users.forms import MyUserUpdateForm


User = get_user_model()


class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = MyUserUpdateForm
    template_name = "users/user_update_form.html"
    success_url = reverse_lazy("dashboard:dashboard")

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs["username"])

    def test_func(self):
        user = self.get_object()
        return user == self.request.user
