from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.views import set_rollback, Response

from .models import ErrorCodes


def handler(exception, context):
    data = dict()

    # 401 Handler
    if isinstance(exception, exceptions.NotAuthenticated):
        exception = UnauthorizedException()

    # 429 Handler
    if isinstance(exception, exceptions.Throttled):
        exception = TooManyRequestsException()

    if isinstance(exception, exceptions.ValidationError):
        # Convert the inconsistent Django error format into a consistent one.
        all_errors = []
        for key, err_details in exception.get_full_details().items():
            for ed in err_details:
                all_errors.append(
                    {
                        "message": ed["message"],
                        "code": ed["code"].value
                        if isinstance(ed["code"], ErrorCodes)
                        else ed["code"],
                    }
                )

        data["errors"] = all_errors
        data["status"] = exception.status_code

        return Response(status=exception.status_code, data=data)

    if isinstance(exception, exceptions.APIException):
        headers = {}

        if getattr(exception, "auth_header", None):
            headers["WWW-Authenticate"] = exception.auth_header
        if getattr(exception, "wait", None):
            headers["Retry-After"] = str(exception.wait)

        data["errors"] = exception.get_full_details()
        data["status"] = exception.status_code

        # Roll back atomic database operations
        set_rollback()

        return Response(headers=headers, status=exception.status_code, data=data)

    # In the case the `exception` is not an APIException return `None`.
    return None


class BadRequestException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 400
    default_detail = _("Invalid request.")


class UnauthorizedException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 401
    default_detail = _("Please sign in.")


class ForbiddenException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 403
    default_detail = _("Forbidden.")


class NotFoundException(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 404
    default_detail = _("Not found.")


class ConflictException(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 409
    default_detail = _("Conflict.")


class PreconditionFailedException(exceptions.APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_code = 412
    default_detail = _("Precondition failed.")


class UnprocessableEntityException(exceptions.APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = 422
    default_detail = _("Unprocessable Entity.")


class TooManyRequestsException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 429
    default_detail = _(
        "You do that a little too often. " "Please wait a little before you try again."
    )


class InternalServerException(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 500
    default_detail = _(
        "Something's gone wrong. "
        "Our technicians are working flat out to solve the problem."
    )
    reason_phrase = default_detail
