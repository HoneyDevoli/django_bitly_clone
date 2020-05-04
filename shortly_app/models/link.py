import random
import re

from django.db import models
from django.conf import settings


class Link(models.Model):
    url = models.URLField(max_length=4048, help_text='Сompression link')
    subpart = models.SlugField(help_text='Enter the desired part of the link', max_length=settings.LENGTH_SUBPART, null=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'url:{}, subpart:{}, create_date:{}'.format(self.url, self.subpart, self.create_date)

    @staticmethod
    def is_unique_subpart(subpart):
        return not Link.objects.filter(subpart=subpart).exists()

    @staticmethod
    def generate_subpart(url):
        length = settings.LENGTH_SUBPART

        letters = re.findall('\\w', url)

        while True:
            subpart = ''.join(random.choice(letters) for i in range(length))

            if Link.is_unique_subpart(subpart):
                return subpart
