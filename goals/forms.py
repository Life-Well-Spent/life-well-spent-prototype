from django import forms
from django.db.models import Q
from django.utils import timezone

from common.utils import get_current_quarter

from .models import GoalModel, MonthEnum, QuarterEnum, StatusEnum, TimeTypeEnum


class GoalForm(forms.Form):
    name = forms.CharField(max_length=255)
    time_type = forms.ChoiceField(
        choices=TimeTypeEnum.choices,
        required=False,
        widget=forms.Select(attrs={"onChange": "OnSelectChange(this)"}),
    )
    parent_goal_year = forms.ModelChoiceField(
        queryset=GoalModel.objects.filter(due_time__type=TimeTypeEnum.YEAR),
        required=False,
        widget=forms.Select(attrs={"onChange": "OnSelectChange(this)"}),
    )
    parent_goal_year_quarter_month = forms.ModelChoiceField(
        queryset=GoalModel.objects.filter(
            Q(due_time__type=TimeTypeEnum.YEAR)
            | Q(due_time__type=TimeTypeEnum.QUARTER)
            | Q(due_time__type=TimeTypeEnum.MONTH)
        ),
        required=False,
        widget=forms.Select(attrs={"onChange": "OnSelectChange(this)"}),
    )
    year = forms.IntegerField(min_value=0, required=False, initial=timezone.now().year)
    quarter = forms.ChoiceField(
        choices=QuarterEnum.choices, required=False, initial=get_current_quarter()
    )
    month = forms.ChoiceField(
        choices=MonthEnum.choices, required=False, initial=timezone.now().month
    )
    week = forms.IntegerField(min_value=1, max_value=52, required=False)
    status = forms.ChoiceField(choices=StatusEnum.choices, required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GoalForm, self).__init__(*args, **kwargs)

        self.fields["parent_goal_year"].label = "Parent goal"
        self.fields["parent_goal_year_quarter_month"].label = "Parent goal"
        self.fields["parent_goal_year"].queryset = self.fields[
            "parent_goal_year"
        ].queryset.filter(user=self.user)
        self.fields["parent_goal_year_quarter_month"].queryset = self.fields[
            "parent_goal_year_quarter_month"
        ].queryset.filter(user=self.user)
