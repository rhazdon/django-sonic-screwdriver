from django import forms
from django.contrib.contenttypes.admin import BaseGenericInlineFormSet

from .models import Comment


class CommentInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentInlineForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)

        self.fields["comment"].widget.attrs["rows"] = 3

        if instance and instance.pk:
            line_height = len(instance.comment.split("\n"))
            self.fields["comment"].widget.attrs["rows"] = line_height
            self.fields["comment"].widget.attrs["readonly"] = True
            self.fields["comment"].widget.attrs["border"] = 0

    class Meta:
        model = Comment
        exclude = []

    class Media:
        css = {"all": ("css/admin_comments.css",)}


class CommentInlineFormset(BaseGenericInlineFormSet):
    def save_new(self, form, commit=True):
        setattr(form.instance, "user", self.current_user)
        return super(CommentInlineFormset, self).save_new(form, commit=True)
