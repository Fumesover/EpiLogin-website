from django.contrib import admin

from website.apps.servers.models import *

class EmailDomainAdmin(admin.ModelAdmin):
    list_display = (
        'domain',
    )

class ServerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )

class RankAdmin(admin.ModelAdmin):
    list_display = (
        'server',
        'type',
        'name',
        'discord_id'
    )

admin.site.register(EmailDomain, EmailDomainAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Rank, RankAdmin)
