from django.db import models
from django.utils.translation import gettext_lazy as _


class QuarterEnum(models.IntegerChoices):
    NONE = 0, _("None")
    Q1 = 1, _("Q1")
    Q2 = 2, _("Q2")
    Q3 = 3, _("Q3")
    Q4 = 4, _("Q4")
