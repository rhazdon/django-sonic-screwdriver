from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django_sonic_screwdriver.models import BaseModel, BaseManager
from django_sonic_screwdriver.settings import api_settings


class BanManager(BaseManager):
    def create_for_user(self, banned_user, end_date=None, *args, **kwargs):
        """
        Creates a ban for an user.
        The default ban time is 1 hour.
        """
        kwargs["banned_user"] = banned_user
        kwargs["end_date"] = end_date if end_date else self.__get_default_end_date()
        return super(BanManager, self).create(*args, **kwargs)

    def create_for_ip(self, ip, end_date=None, *args, **kwargs):
        """
        Creates a ban for an ip.
        The default ban time is 1 hour.
        """
        kwargs["ip"] = ip
        kwargs["end_date"] = end_date if end_date else self.__get_default_end_date()
        return super(BanManager, self).create(*args, **kwargs)

    @staticmethod
    def __get_default_end_date():
        return timezone.now() + timezone.timedelta(
            seconds=api_settings.BAN_DEFAULT_END_TIME
        )


class Ban(BaseModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        blank=False,
        null=True,
        help_text=(
            "This is the creator of the ban. "
            "If the creator is empty, the ban was created by the system."
        ),
    )

    end_date = models.DateTimeField(
        verbose_name=_("End date of the ban"),
        blank=True,
        null=True,
        help_text=_(
            "The end date tells, until the ban is valid. "
            "If the end_date is empty, the ban is infinit."
        ),
    )

    objects = BanManager()

    class Meta:
        abstract = True
        verbose_name = _("Ban")
        verbose_name_plural = _("Bans")


class UserBan(Ban):
    banned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="banned_user",
        blank=False,
        null=True,
        help_text="This is the banned user or the receiver of the ban.",
    )

    class Meta:
        verbose_name = _("User Ban")
        verbose_name_plural = _("User Bans")

    def __str__(self):
        return self.banned_user.get_username()


class IPBan(Ban):
    ip = models.GenericIPAddressField(
        verbose_name=_("IP"),
        blank=False,
        null=True,
        help_text=_(
            "This is the banned ip. Every request from this IP will result in 403."
        ),
    )

    class Meta:
        verbose_name = _("IP Ban")
        verbose_name_plural = _("IP Bans")

    def __str__(self):
        return str(self.ip)
