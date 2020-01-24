from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_sonic_screwdriver.admin import BaseModelAdmin

from .models import UserBan, IPBan


@admin.register(UserBan)
class UserBanAdmin(BaseModelAdmin):  # pragma: no cover
    fieldsets = (
        (_("Ban"), {"fields": ("banned_user", "end_date")}),
    ) + BaseModelAdmin.fieldsets


@admin.register(IPBan)
class IPBanAdmin(BaseModelAdmin):  # pragma: no cover
    fieldsets = ((_("Ban"), {"fields": ("ip", "end_date")}),) + BaseModelAdmin.fieldsets
