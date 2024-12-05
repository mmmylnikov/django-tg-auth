from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from config.settings import DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tgauth.urls')),
]

if DEBUG:
    urlpatterns += staticfiles_urlpatterns()  # type: ignore
