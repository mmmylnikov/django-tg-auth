from dataclasses import dataclass

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AbstractGroup
from django.db import models


class Group(AbstractGroup):
    '''
    The Group model, If it needs to be expanded in the future
    '''
    pass


@dataclass
class UserBio:
    id: int
    username: str
    first_name: str
    last_name: str
    photo_url: str | None


class User(AbstractUser):
    tg_id = models.BigIntegerField(
        unique=True, null=True, blank=True, verbose_name="Telegram ID"
    )
    tg_photo_url = models.URLField(
        null=True, blank=True, verbose_name="Telegram photo URL"
    )

    @property
    def tg_account(self) -> SocialAccount | None:
        tg_account = SocialAccount.objects.filter(
            user=self, provider="telegram"
        ).first()
        if not tg_account:
            return None
        return tg_account

    @property
    def bio(self) -> UserBio:
        tg_account = self.tg_account
        if not tg_account:
            return UserBio(
                id=self.pk,
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                photo_url=None,
            )
        return UserBio(
            id=tg_account.extra_data['id'],
            username=tg_account.extra_data['username'],
            first_name=tg_account.extra_data['first_name'],
            last_name=tg_account.extra_data['last_name'],
            photo_url=tg_account.extra_data['photo_url'],
        )
