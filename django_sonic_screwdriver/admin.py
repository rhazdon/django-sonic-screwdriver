from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse("admin:{}_{}_change".format(app_label, model_name), args=(obj.pk,))


def admin_link(attr, short_description, empty_description="-"):
    """
    Decorator used for rendering a link to a related model in the admin detail page.
    attr (str):
        Name of the related field.
    short_description (str):
        Name if the field.
    empty_description (str):
        Value to display if the related field is None.
    The wrapped method receives the related object and should
    return the link text.
    Usage:
        @admin_link('credit_card', _('Credit Card'))
        def credit_card_link(self, credit_card):
            return credit_card.name
    """

    def wrap(func):
        def field_func(self, obj):
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_change_url(related_obj)
            return format_html('<a href="{}">{}</a>', url, func(self, related_obj))

        field_func.short_description = short_description
        field_func.allow_tags = True
        return field_func

    return wrap


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base Model Admin
    Describes the default values of nearly every Model.

    Note: Model must inherit BaseGameModel!
    """

    fieldsets = ((_("Created and Updated"), {"fields": ("created_at", "updated_at")}),)
    readonly_fields = ("created_at", "updated_at")
    list_display = ("__str__", "created_at", "updated_at")

    def get_ordering(self, request):
        return ["-created_at"]


class BaseStackedInlineAdmin(admin.StackedInline):
    """
    Model: BaseStackedInlineAdmin

    Usable for inline stacks.

    For inline values over foreign keys.
    This model is also usable for ManyToMany relations.
    """

    readonly_fields = ("created_at", "updated_at")
    min_num = 0
    extra = 0
    show_change_link = True


class BaseTabularInlineAdmin(admin.TabularInline):
    """
    Model: BaseTabularInlineAdmin

    Usable for inline stacks.

    For inline values over foreign keys.
    This model is also usable for ManyToMany relations.
    """

    readonly_fields = ("created_at", "updated_at")
    min_num = 0
    extra = 0
    show_change_link = True


class ReadAndDeleteOnlyAdminMixin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False


class ReadOnlyAdminMixin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
