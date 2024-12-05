from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup

from user.models import Group, User


class GroupAdmin(BaseGroupAdmin):
    """The default model. Expand if necessary."""
    pass


class UserAdmin(BaseUserAdmin):
    """The default model. Expand if necessary."""
    pass


admin.site.unregister(BaseGroup)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
