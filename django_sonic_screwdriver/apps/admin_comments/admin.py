from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import CommentInlineForm, CommentInlineFormset
from .models import Comment


class CommentInline(GenericTabularInline):
    model = Comment

    readonly_fields = ["user", "created_at"]

    def __init__(self, *args, **kwargs):
        self.form = CommentInlineForm
        self.formset = CommentInlineFormset
        self.extra = 1
        super(CommentInline, self).__init__(*args, **kwargs)

    def get_queryset(self, request):
        return super(CommentInline, self).get_queryset(request).order_by("-created_at")

    def has_delete_permission(self, request, obj=None):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CommentInline, self).get_formset(request, obj, **kwargs)
        formset.current_user = request.user
        return formset
