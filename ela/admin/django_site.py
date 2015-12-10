from django.contrib import admin
from ela.sites import main_admin_site
from django.contrib.sites.models import Site

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')

main_admin_site.register(Site, SiteAdmin)
