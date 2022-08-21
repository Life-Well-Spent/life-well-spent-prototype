from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeTypeEnum(models.TextChoices):
    NONE = "", _("None")
    YEAR = "Y", _("Year")
    QUARTER = "Q", _("Quarter")
    MONTH = "M", _("Month")
    WEEK = "W", _("Week")
