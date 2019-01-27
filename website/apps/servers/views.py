from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from website.apps.servers.models import Server
from website.apps.members.models import Member
from website.apps.groups.models  import Group

class info(View):
    @method_decorator(login_required)
    def get(self, request, server_id):
        context = {
            'user': request.user,
            'user_extra': request.user.social_auth.get(provider="discord").extra_data,
            'server': get_object_or_404(Server, server_id=server_id),
        }

        return render(request, "servers/info.html", context)

@method_decorator(csrf_exempt, name='dispatch')
class update(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        for key,value in data['servers'].items():
            server, created = Server.objects.get_or_create(
                server_id=key,
                defaults={'name': value['name']}
            )

        for key,value in data['members'].items():
            member, created = Member.objects.get_or_create(
                id=key,
            )

            member.username = value['name']
            member.login = value['login']
            member.save()

            for server_id in value['servers']:
                server = Server.objects.get(
                    server_id=server_id
                )

                server.members.add(member)

        for group in data['groups']:
            group, created = Group.objects.get_or_create(
                group=group['group'],
                login=group['login'],
            )

        return HttpResponse('')
