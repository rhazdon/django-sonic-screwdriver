from django.utils.translation import ugettext_lazy as _

from django_sonic_screwdriver.admin import BaseModelAdmin


class UserBanAdmin(BaseModelAdmin):  # pragma: no cover
    fieldsets = (
        (_("Ban"), {"fields": ("banned_user", "end_date")}),
    ) + BaseModelAdmin.fieldsets
    readonly_fields = BaseModelAdmin.readonly_fields + ("user",)


class IPBanAdmin(BaseModelAdmin):  # pragma: no cover
    fieldsets = ((_("Ban"), {"fields": ("ip", "end_date")}),) + BaseModelAdmin.fieldsets
    readonly_fields = BaseModelAdmin.readonly_fields + ("ip",)
