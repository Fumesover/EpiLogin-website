from django.contrib import admin

from website.apps.members.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hash',
        'email'
    )

admin.site.register(Member, MemberAdmin)
