from django.db import models
from django.utils.translation import ugettext_lazy as _
from enum import Enum


class BaseManager(models.Manager):
    def get_or_404(self, *args, **kwargs):
        """
        Returns instance or raises 404.
        """
        try:
            instance = super(BaseManager, self).get(*args, **kwargs)
        except self.model.DoesNotExist:
            from .exceptions import NotFoundException

            raise NotFoundException
        return instance


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
        blank=False,
        null=False,
        help_text=_("Model was created at this time."),
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
        blank=False,
        null=False,
        help_text=_("Model was updated at this time."),
    )

    objects = BaseManager()

    class Meta:
        abstract = True


class BaseChoiceEnum(Enum):
    def __str__(self):
        return self.name

    @classmethod
    def as_choices(cls):
        return [(tag.name, tag.value) for tag in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name_for_value(cls, value, default=None):
        status = cls._value2member_map_.get(value, default)
        return status.name if status else default


class ErrorCodes(Enum):

    def __str__(self):
        return str(self.value)