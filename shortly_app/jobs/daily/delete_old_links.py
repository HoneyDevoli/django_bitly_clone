from datetime import datetime, timedelta
import logging

from django_extensions.management.jobs import DailyJob

from shortly_app.models import Link


logger = logging.getLogger(__name__)

class Job(DailyJob):
    """Daily removes links, leaving only the last 30 days"""

    def execute(self):
        logger.info('starting a daily task to remove links older than 30 days')

        first_date = Link.objects.all().order_by('-create_date').last().create_date
        last_day = datetime.now() - timedelta(days=30)

        links = Link.objects.filter(create_date__range=[first_date, last_day])
        links_count = links.count()
        links.delete()

        logger.info('{} links were deleted by date between {} and {}'.format(links_count, first_date, last_day))

