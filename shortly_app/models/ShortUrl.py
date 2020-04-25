from django.db.models import Model, CharField, DateField


class ShortUrl(Model):
    url = CharField(max_length=4048)
    short_url = CharField(max_length=200)
    create_date = DateField()
