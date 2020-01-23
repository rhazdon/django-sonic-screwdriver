from django.conf import settings
from django.contrib.auth import get_user
from django.db.models import Q
from django.utils import timezone

from django_sonic_screwdriver.exceptions import ForbiddenException

from .models import UserBan, IPBan


class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self._before_view(request)
        response = self.get_response(request)
        request, response = self._after_view(request, response)
        return response

    def _before_view(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.

        :param request:
        :return:
        """
        self.__check_for_user_bans(request)
        self.__check_for_ip_bans(request)
        return request

    def _after_view(self, request, response):
        """
        Code to be executed for each request/response after
        the view is called.

        :param request:
        :param response:
        :return:
        """
        return request, response

    def __check_for_user_bans(self, request):
        """
        Get the user and try to find a ban for the user.

        :param: request
        """
        user = get_user(request)
        bans = UserBan.objects.filter(banned_user=user).filter(
            Q(end_date__gte=timezone.now()) | Q(end_date__exact=None)
        )

        if bans:
            raise ForbiddenException()

    def __check_for_ip_bans(self, request):
        """
        Get the ip_address of the request and try to find a ban
        with this ip.

        :param: request
        """
        ip_address = request.META.get(
            settings.DJANGO_SONIC_SCREWDRIVER_BAN_REMOTE_ADDR_HEADER
        )
        bans = IPBan.objects.filter(ip=ip_address).filter(
            Q(end_date__gte=timezone.now()) | Q(end_date__exact=None)
        )

        if bans:
            raise ForbiddenException()
