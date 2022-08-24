from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from goals.models.goal import GoalModel


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/settings.html"


class DeleteAccountView(View):
    def post(self, request):
        goals = GoalModel.objects.filter(user=self.request.user)
        for goal in goals:
            goal.delete()

        self.request.user.delete()

        return HttpResponseRedirect(reverse("home"))
