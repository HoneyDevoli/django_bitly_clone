from django.contrib import admin

from shortly_app.models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ['url', 'subpart', 'create_date']
    fields = ['url', 'subpart', 'create_date']
    readonly_fields = ['create_date']


admin.site.register(Link, LinkAdmin)
