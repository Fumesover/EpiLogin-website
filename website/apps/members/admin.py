from django.contrib import admin

from website.apps.members.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hash',
        'login'
    )

admin.site.register(Member, MemberAdmin)
