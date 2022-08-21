from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView

from .forms import GoalForm
from .models import GoalModel, StatusEnum, TimeModel


class GoalListView(LoginRequiredMixin, ListView):
    model = GoalModel
    context_object_name = "goal_list"
    paginate_by = 10
    ordering = "-modified"

    class Meta:
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(GoalListView, self).get_context_data(*args, **kwargs)
        context["create_form"] = GoalForm(self.request.user)
        context["update_forms"] = {}

        for object in GoalModel.objects.filter(user=self.request.user):
            data = {
                "name": object.name,
                "time_type": object.due_time.type,
                "parent_goal_year": object.parent_goal,
                "parent_goal_quarter_or_month": object.parent_goal,
                "year": object.due_time.year,
                "quarter": object.due_time.quarter,
                "month": object.due_time.month,
                "week": object.due_time.week,
                "status": object.status,
            }
            context["update_forms"][object.id] = GoalForm(
                initial=data, user=self.request.user
            )

        context["status_choices"] = dict(StatusEnum.choices).items
        return context

    def get_form_kwargs(self):
        user = self.request.user
        form_kwargs = super(GoalListView, self).get_form_kwargs()
        form_kwargs.update({"user": user})
        return form_kwargs

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query is None:
            return self.object_list.order_by(self.ordering).filter(
                user=self.request.user
            )

        return self.object_list.filter(Q(name__icontains=query))


class BackLogView(GoalListView):
    template_name = "goals/lists/backlog_goal_list.html"
    object_list = GoalListView.model.objects.is_backlog()


class PlannedView(GoalListView):
    template_name = "goals/lists/planned_goal_list.html"
    object_list = GoalListView.model.objects.is_planned()


class CurrentView(GoalListView):
    template_name = "goals/lists/current_goal_list.html"
    object_list = GoalListView.model.objects.is_current()


class ArchiveView(GoalListView):
    template_name = "goals/lists/archive_goal_list.html"
    object_list = GoalListView.model.objects.is_archive()


class CreateView(View):
    def post(self, request):
        data = get_post_data(request.POST, request.user)
        next = request.POST["next"]

        time = TimeModel(
            type=data["time_type"],
            year=data["year"],
            quarter=data["quarter"],
            month=data["month"],
            week=data["week"],
        )
        time.save()

        goal = GoalModel(
            name=data["name"],
            status=data["status"],
            parent_goal=data["parent_goal"],
            due_time=time,
            user=request.user,
        )
        goal.save()

        return HttpResponseRedirect(next)


class UpdateView(View):
    def post(self, request, pk):
        data = get_post_data(request.POST, request.user)
        next = request.POST["next"]

        goal = GoalModel.objects.get(user=request.user, pk=pk)
        if goal is None:
            return Http404("Goal does not exist.")

        if not request.POST.get("status_update", None):
            goal.due_time.type = data["time_type"]
            goal.due_time.year = data["year"]
            goal.due_time.quarter = data["quarter"]
            goal.due_time.month = data["month"]
            goal.due_time.week = data["week"]

            goal.due_time.save()

            goal.name = data["name"]
            goal.parent_goal = data["parent_goal"]

        goal.status = data["status"]

        goal.save()

        return HttpResponseRedirect(next)


class DeleteView(View):
    def get(self, request, pk, next):

        goal = GoalModel.objects.get(user=request.user, pk=pk)
        if goal is None:
            return Http404("Goal does not exist.")

        goal.delete()

        return HttpResponseRedirect(next)


def get_post_data(data, user):
    result = {}

    name = data.get("name", None)
    time_type = data.get("time_type", None)
    parent_goal_year_id = data.get("parent_goal_year", None)
    parent_goal_quarter_or_month_id = data.get("parent_goal_quarter_or_month", None)
    year = data.get("year", None)
    quarter = data.get("quarter", None)
    month = data.get("month", None)
    week = data.get("week", None)
    status = data.get("status", None)

    parent_goal = None
    if parent_goal_year_id:
        parent_goal_year = GoalModel.objects.filter(user=user).get(
            pk=parent_goal_year_id
        )

        parent_goal = parent_goal_year
        year = parent_goal_year.due_time.year

    if parent_goal_quarter_or_month_id:
        parent_goal_quarter_or_month = GoalModel.objects.filter(user=user).get(
            pk=parent_goal_quarter_or_month_id
        )

        parent_goal = parent_goal_quarter_or_month
        year = parent_goal_quarter_or_month.due_time.year
        quarter = parent_goal_quarter_or_month.due_time.quarter
        month = parent_goal_quarter_or_month.due_time.month

    result["name"] = None if name == "" else name
    result["time_type"] = None if time_type == "" else time_type
    result["parent_goal"] = parent_goal
    result["year"] = None if year == "" else year
    result["quarter"] = None if quarter == "" else quarter
    result["month"] = None if month == "" else month
    result["week"] = None if week == "" else week
    result["status"] = None if status == "" else status

    return result
