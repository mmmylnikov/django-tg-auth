from typing import Any

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from config.settings import DJANGO_TELEGRAM_USERNAME, LOGIN_REDIRECT_URL
from tgauth.utils import TgDataCheckString, get_or_create_user


class IndexView(LoginRequiredMixin, RedirectView):
    pattern_name = "tgauth-profile"
    permanent = False
    query_string = True


class TgAuthView(TemplateView):
    template_name = "tgauth/auth.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # For Telegram Login Widget
        # https://core.telegram.org/widgets/login
        context["tg_bot_username"] = DJANGO_TELEGRAM_USERNAME
        context["tg_bot_auth_redirect"] = reverse(LOGIN_REDIRECT_URL)
        return context


class TgProfileView(TemplateView):
    template_name = "tgauth/profile.html"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if request.user.is_anonymous:
            if not TgDataCheckString.from_GET(request.GET).check_hash():
                raise BadRequest("Invalid hash")
            user, _ = get_or_create_user(request=request)
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
        return super().get(request, *args, **kwargs)


class TgLogoutView(LogoutView):
    pass
