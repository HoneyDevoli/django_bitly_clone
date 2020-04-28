from datetime import datetime, timedelta

from django.utils import timezone
from django_extensions.management.jobs import DailyJob

from shortly_app.models import Link


class Job(DailyJob):

    def execute(self):
        print('starting a daily task to remove links older than 30 days')

        first_date = Link.objects.all().order_by('-create_date').last().create_date
        last_day = datetime.now() - timedelta(days=30)

        links = Link.objects.filter(create_date__range=[first_date, last_day])
        links_count = links.count()
        links.delete()

        print('{} links were deleted by date between {} and {}'.format(links_count, first_date, last_day))

