from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
import json

from website.apps.servers.models import Server
from website.apps.members.models import Member
from website.apps.groups.models  import Group, Ban, Update

class deleteban(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        ban = get_object_or_404(Ban, pk=pk)

        server_id = ban.server.server_id

        Update(
            server=ban.server,
            type='unban',
            ban_type=ban.type,
            value=ban.value
        ).save()

        ban.delete()

        return redirect('servers:info', server_id=server_id)

class deletegroup(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        login = group.login

        member = get_object_or_404(Member, login=login)

        Update(
            type='delgroup',
            login=group.login,
            value=group.group,
        ).save()

        group.delete()

        return redirect('members:profile', id=member.id)
