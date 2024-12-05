import hashlib
import hmac
import time
from dataclasses import dataclass
from urllib.parse import quote

from allauth.socialaccount.models import SocialAccount
from django.http.request import HttpRequest, QueryDict
from django.urls import reverse

from config.settings import (
    DJANGO_HOST,
    DJANGO_TELEGRAM_SECRET,
    LOGIN_REDIRECT_URL,
)
from user.models import User


@dataclass
class TgDataCheckString:
    id: str
    username: str
    first_name: str
    last_name: str
    photo_url: str
    auth_date: str
    hash: str

    @staticmethod
    def from_now_date(
        id: str, username: str, first_name: str, last_name: str, photo_url: str
    ) -> "TgDataCheckString":
        unix_timestamp = int(time.time())
        obj = TgDataCheckString(
            id=id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url,
            auth_date=str(unix_timestamp),
            hash=''
        )
        obj.hash = obj.get_hash_by_msg(obj.get_checked_string())
        return obj

    @staticmethod
    def from_GET(querydict: QueryDict) -> "TgDataCheckString":
        # this block checks for type errors that are ignored further
        for k, v in querydict.items():
            if isinstance(v, str):
                continue
            raise TypeError
        return TgDataCheckString(
            id=querydict["id"],  # type: ignore[arg-type]
            username=querydict["username"],  # type: ignore[arg-type]
            first_name=querydict["first_name"],  # type: ignore[arg-type]
            last_name=querydict["last_name"],  # type: ignore[arg-type]
            photo_url=querydict["photo_url"],  # type: ignore[arg-type]
            auth_date=querydict["auth_date"],  # type: ignore[arg-type]
            hash=querydict["hash"],  # type: ignore[arg-type]
        )

    def get_checked_string(self) -> str:
        return "\n".join(
            f"{k}={v}" for k, v in sorted(self.__dict__.items()) if k != "hash"
        )

    def get_hash_by_msg(self, msg: str) -> str:
        if not DJANGO_TELEGRAM_SECRET:
            raise Exception("DJANGO_TELEGRAM_SECRET is not set")
        return hmac.new(
            key=hashlib.sha256(
                DJANGO_TELEGRAM_SECRET.encode("utf-8")
            ).digest(),
            msg=msg.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    def check_hash(self) -> bool:
        hash_value_response = self.hash
        data_check_string = self.get_checked_string()
        hash_value_correct = self.get_hash_by_msg(data_check_string)
        return hash_value_response == hash_value_correct

    def auth_url(self) -> str:
        url = DJANGO_HOST + reverse(LOGIN_REDIRECT_URL, ) + '?'
        args = ''
        for k, v in self.__dict__.items():
            args += f"{k}={v}&"
        else:
            args = quote(args[:-1], safe="=&")
        return url + args


def get_or_create_regular_user(request: HttpRequest) -> tuple[User, bool]:
    user, user_created = User.objects.get_or_create(
        username=request.GET["username"],
        first_name=request.GET["first_name"],
        last_name=request.GET["last_name"],
    )
    return user, user_created


def get_or_create_tg_user(
    request: HttpRequest, user: User
) -> tuple[User, bool]:
    tg_user, tg_user_created = SocialAccount.objects.get_or_create(
        user=user,
        provider="telegram",
        uid=request.GET["id"],
        extra_data={
            "id": request.GET["id"],
            "username": request.GET["username"],
            "first_name": request.GET["first_name"],
            "last_name": request.GET["last_name"],
            "photo_url": request.GET["photo_url"],
        },
    )
    return tg_user, tg_user_created


def get_or_create_user(request: HttpRequest) -> tuple[User, bool]:
    user, user_created = get_or_create_regular_user(request)
    if not user_created:
        return user, user_created
    get_or_create_tg_user(request, user)
    return user, user_created
