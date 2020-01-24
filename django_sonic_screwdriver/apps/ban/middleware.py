from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.utils import timezone

from django_sonic_screwdriver.settings import api_settings

from .models import UserBan, IPBan


class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self._before_view(request)
        if isinstance(request, HttpResponseForbidden):
            return request

        response = self.get_response(request)
        request, response = self._after_view(request, response)
        return response

    def bans_found_action(self):
        return HttpResponseForbidden()

    def _before_view(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.

        :param request:
        :return:
        """
        if self.__user_ban_exists(request) or self.__ip_ban_exists(request):
            return self.bans_found_action()
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

    def __user_ban_exists(self, request):
        """
        Get the user and try to find a ban for the user.

        :param: request
        """
        if not isinstance(request.user, AnonymousUser):
            return (
                UserBan.objects.filter(banned_user=request.user)
                .filter(Q(end_date__gte=timezone.now()) | Q(end_date__exact=None))
                .exists()
            )

    def __ip_ban_exists(self, request):
        """
        Get the ip_address of the request and try to find a ban
        with this ip.

        :param: request
        """
        ip_address = request.META.get(api_settings.BAN_REMOTE_ADDR_HEADER)
        return (
            IPBan.objects.filter(ip=ip_address)
            .filter(Q(end_date__gte=timezone.now()) | Q(end_date__exact=None))
            .exists()
        )
