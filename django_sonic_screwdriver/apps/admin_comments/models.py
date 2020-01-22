from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_sonic_screwdriver.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        blank=False,
        null=True,
        help_text=_("The user is the creator of the comment."),
    )

    comment = models.TextField(
        verbose_name=_("Comment"),
        blank=False,
        null=True,
        help_text=_("The comment itself."),
    )

    object_id = models.CharField(
        max_length=36,
        verbose_name=_("Object ID"),
        blank=True,
        null=True,
        help_text=_("ID of the related object."),
    )

    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="object_id", for_concrete_model=True
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content type"),
        blank=False,
        null=True,
        help_text=_("Related content type."),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.content_type} - {self.object_id}"
