from django.contrib import admin

from website.apps.groups.models import Group, Ban, Update

class GroupsAdmin(admin.ModelAdmin):
    list_display = (
        'group',
        'login'
    )

class BansAdmin(admin.ModelAdmin):
    list_display = (
        'server',
        'type',
        'value'
    )

class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        'server',
        'type',
        'ban_type',
        'value'
    )

admin.site.register(Group, GroupsAdmin)
admin.site.register(Ban, BansAdmin)
admin.site.register(Update, UpdateAdmin)
