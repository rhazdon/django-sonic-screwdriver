from django.test import TestCase
from django.contrib.auth import get_user_model

from django_sonic_screwdriver.apps.ban.models import UserBan, IPBan
from django_sonic_screwdriver.exceptions import ForbiddenException

User = get_user_model()


class AppBanTest(TestCase):
    def test_user_ban_create(self):
        user = User.objects.create(username="test", password="123")
        UserBan.objects.create(banned_user=user)
        self.assertEqual(UserBan.objects.count(), 1)

    def test_banned_user_will_receive_403(self):
        user = User.objects.create(username="test", password="123")
        self.client.force_login(user)

        res = self.client.get("/home/")
        self.assertEqual(res.status_code, 200)

        UserBan.objects.create_for_user(banned_user=user)

        with self.assertRaises(ForbiddenException):
            res = self.client.get("/home/")
            self.assertEqual(res.status_code, 403)

    def test_banned_ip_will_receive_403(self):
        user = User.objects.create(username="test", password="123")
        self.client.force_login(user)

        res = self.client.get("/home/", REMOTE_ADDR="127.0.0.1")
        self.assertEqual(res.status_code, 200)

        IPBan.objects.create_for_ip(ip="127.0.0.1")

        with self.assertRaises(ForbiddenException):
            res = self.client.get("/home/", **{"REMOTE_ADDR": "127.0.0.1"})
            self.assertEqual(res.status_code, 403)
