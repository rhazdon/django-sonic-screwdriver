from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_sonic_screwdriver.apps.admin_comments.models import Comment


class CommentTest(TestCase):
    def test_str_repr(self):
        content_type = ContentType.objects.first()
        comment = Comment.objects.create(
            comment="Test", object_id="123", content_type=content_type
        )
        self.assertEqual(str(comment), f"{content_type} - {comment.object_id}")
