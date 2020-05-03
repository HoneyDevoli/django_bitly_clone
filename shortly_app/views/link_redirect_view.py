from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
import redis

from shortly.settings import REDIS_CACHE_TIMEOUT_HOURS, REDIS_HOST, REDIS_PORT
from shortly_app.models import Link


class LinkRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        rds = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        subpart = kwargs['subpart']

        url = rds.get(subpart)
        if not url:
            link = get_object_or_404(Link, subpart=subpart)
            url = link.url
            rds.setex(subpart,
                      timedelta(hours=REDIS_CACHE_TIMEOUT_HOURS),
                      value=url)

        return url
