from django.urls import include, path

from tgauth.views import IndexView, TgAuthView, TgLogoutView, TgProfileView


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view(), name='tgauth-index'),
    path('login/', TgAuthView.as_view(), name='tgauth-login'),
    path('logout/', TgLogoutView.as_view(), name='tgauth-logout'),
    path('profile/', TgProfileView.as_view(), name='tgauth-profile'),
]
