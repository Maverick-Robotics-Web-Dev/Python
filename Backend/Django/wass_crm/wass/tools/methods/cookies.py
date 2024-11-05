from typing import Any

from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.utils import timezone

from rest_framework.response import Response

from rest_framework_simplejwt.settings import api_settings as jwt_settings

from core.settings import CACV_KEY

sensitive_post_parameters_method = method_decorator(sensitive_post_parameters('password', 'new_password',),)


def set_jwt_access_cookie(response: Response, access_token: Any) -> None:

    cookie_name: Any = CACV_KEY.get('JWT_AUTH_COOKIE')
    access_token_expiration: Any = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
    cookie_secure: Any = CACV_KEY.get('JWT_AUTH_SECURE')
    cookie_httponly: Any = CACV_KEY.get('JWT_AUTH_HTTPONLY')
    cookie_samesite: Any = CACV_KEY.get('JWT_AUTH_SAMESITE')
    cookie_domain: Any = CACV_KEY.get('JWT_AUTH_COOKIE_DOMAIN')

    if cookie_name:
        response.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            domain=cookie_domain,
        )


def set_jwt_refresh_cookie(response: Response, refresh_token: Any) -> None:

    refresh_token_expiration: Any = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
    refresh_cookie_name: Any = CACV_KEY.get('JWT_AUTH_REFRESH_COOKIE')
    refresh_cookie_path: Any = CACV_KEY.get('JWT_AUTH_REFRESH_COOKIE_PATH')
    cookie_secure: Any = CACV_KEY.get('JWT_AUTH_SECURE')
    cookie_httponly: Any = CACV_KEY.get('JWT_AUTH_HTTPONLY')
    cookie_samesite: Any = CACV_KEY.get('JWT_AUTH_SAMESITE')
    cookie_domain: Any = CACV_KEY.get('JWT_AUTH_COOKIE_DOMAIN')

    if refresh_cookie_name:
        response.set_cookie(
            refresh_cookie_name,
            refresh_token,
            expires=refresh_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            path=refresh_cookie_path,
            domain=cookie_domain,
        )


def set_jwt_cookies(response: Response, access_token: Any, refresh_token: Any) -> None:

    set_jwt_access_cookie(response, access_token)
    set_jwt_refresh_cookie(response, refresh_token)


def unset_jwt_cookies(response: Response) -> None:

    cookie_name: Any = CACV_KEY.get('JWT_AUTH_COOKIE')
    refresh_cookie_name: Any = CACV_KEY.get('JWT_AUTH_REFRESH_COOKIE')
    refresh_cookie_path: Any = CACV_KEY.get('JWT_AUTH_REFRESH_COOKIE_PATH')
    cookie_samesite: Any = CACV_KEY.get('JWT_AUTH_SAMESITE')
    cookie_domain: Any = CACV_KEY.get('JWT_AUTH_COOKIE_DOMAIN')

    if cookie_name:
        response.delete_cookie(cookie_name, samesite=cookie_samesite, domain=cookie_domain)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name, path=refresh_cookie_path, samesite=cookie_samesite, domain=cookie_domain)
