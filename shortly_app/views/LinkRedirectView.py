from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

from shortly_app.models import Link


class LinkRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, subpart=kwargs['subpart'])
        return link.url
