from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusEnum(models.TextChoices):
    NONE = "", _("None")
    WIP = "W", _("WIP")
    DONE = "D", _("Done")
    CANCELLED = "C", _("Cancelled")
