from django.conf import settings
from django.urls import path, re_path

from .views import HomeView
from .views import LinkRedirectView

urlpatterns = [
    re_path(r'^(?P<subpart>\w{1,%d})$' % settings.LENGTH_SUBPART, LinkRedirectView.as_view()),
    path('', HomeView.as_view()),
]

