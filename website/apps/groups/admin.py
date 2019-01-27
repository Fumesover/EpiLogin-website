from django.contrib import admin

from website.apps.groups.models import Group

class GroupsAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'login'
    )

admin.site.register(Group, GroupsAdmin)
