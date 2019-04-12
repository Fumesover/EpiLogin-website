from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse

from website.apps.servers.models import Server
from website.apps.members.models import Member
from website.apps.groups.models  import Group, Ban, Update

class deleteban(View):
    @method_decorator(login_required)
    @method_decorator(permission_required('groups.delete_ban'))
    def get(self, request, pk):
        ban = get_object_or_404(Ban, pk=pk)
        server = ban.server

        if not request.user.is_superuser and not request.user in server.moderators.all() and not request.user in server.admins.all():
            raise Http404('Not found')

        Update(
            server=server,
            type='unban',
            ban_type=ban.type,
            value=ban.value
        ).save()

        ban.delete()

        return redirect('servers:info', pk=server.pk)

class deletegroup(View):
    @method_decorator(login_required)
    @method_decorator(permission_required('groups.delete_group'))
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        email = group.email

        member = get_object_or_404(Member, email=email)

        Update(
            type='delgroup',
            email=group.email,
            value=group.group,
        ).save()

        group.delete()

        return redirect('members:profile', id=member.id)

class updates(View):
    @method_decorator(login_required)
    def get(self, request):
        return redirect('')
