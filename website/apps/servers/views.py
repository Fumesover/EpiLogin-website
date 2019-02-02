from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from basicauth.decorators import basic_auth_required
import json

from website.apps.servers.models import Server
from website.apps.members.models import Member
from website.apps.groups.models  import Group, Ban, Update

class info(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, server_id):
        server = get_object_or_404(Server, server_id=server_id)
        bans = {
            'users': Ban.objects.filter(server=server, type='user'),
            'groups': Ban.objects.filter(server=server, type='group'),
            'logins': Ban.objects.filter(server=server, type='login'),
        }

        context = {
            'user': request.user,
            'user_extra': request.user.social_auth.get(provider="discord").extra_data,
            'server': server,
            'bans': bans,
        }

        return render(request, "servers/info.html", context)

class list(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        context = {
            'user': request.user,
            'user_extra': request.user.social_auth.get(provider="discord").extra_data,
            'servers': Server.objects.all()
        }

        return render(request, "servers/list.html", context)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(basic_auth_required, name='dispatch')
class update(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        for key,value in data['servers'].items():
            server, created = Server.objects.get_or_create(
                server_id=key,
                defaults={'name': value['name']}
            )

            for ban in value['bans']:
                ban, created = Ban.objects.get_or_create(
                    server = server,
                    type  = ban['type'],
                    value = ban['data']
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

    def get(self, request):
        updates = Update.objects.all()

        data = {
            'unban': [],
            'ban':   [],
            'addgroup': [],
            'delgroup': [],
            'certify': [],
        }

        for update in updates:
            if update.type == 'unban':
                data['unban'].append({
                    'pk': update.pk,
                    'server': update.server.server_id,
                    'ban_type': update.ban_type,
                    'value': update.value,
                })
            elif update.type == 'ban':
                data['ban'].append({
                    'pk': update.pk,
                    'server': update.server.server_id,
                    'ban_type': update.ban_type,
                    'value': update.value,
                })
            elif update.type == 'addgroup':
                data['addgroup'].append({
                    'pk':    update.pk,
                    'login': update.login,
                    'value': update.value,
                })
            elif update.type == 'delgroup':
                data['delgroup'].append({
                    'pk':    update.pk,
                    'login': update.login,
                    'value': update.value,
                })
            elif update.type == 'certify':
                data['certify'].append({
                    'pk':    update.pk,
                    'login': update.login,
                    'value': update.value,
                })
            else:
                print(update.type)

        return JsonResponse(data)

    def delete(self, request):
        for pk in json.loads(request.body)['pk']:
            try:
                Update.objects.get(
                    pk=pk
                ).delete()
            except Exception:
                pass

        return HttpResponse('')

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(basic_auth_required, name='dispatch')
class push(View):
    def post(self, request):
        data = json.loads(request.body)

        if 'addgroup' in data:
            for addgroup in data['addgroup']:
                group, created = Group.objects.get_or_create(
                    login=addgroup['login'],
                    group=addgroup['group']
                )

        if 'delgroup' in data:
            for delgroup in data['delgroup']:
                groups = Group.objects.filter(
                    login=delgroup['login'],
                    group=delgroup['group']
                )

                for group in groups:
                    group.delete()

        if 'bans' in data:
            server = get_object_or_404(Server, server_id=data['bans']['server'])
            for ban in data['bans']['banned']:
                ban, created = Ban.objects.get_or_create(
                    server=server,
                    type=data['bans']['type'],
                    value=ban
                )

        if 'unbans' in data:
            server = get_object_or_404(Server, server_id=data['unbans']['server'])
            for ban in data['unbans']['unbanned']:
                ban = Ban.objects.get(
                    server=server,
                    type=data['unbans']['type'],
                    value=ban
                )
                if ban: ban.delete()

        if 'certify' in data:
            member, created = Member.objects.get_or_create(
                id=data['certify']['id']
            )
            member.login = data['certify']['login']
            member.save()

        if 'joined' in data:
            member, created = Member.objects.get_or_create(
                id=data['joined']['id']
            )

            member.username = data['joined']['username']
            member.save()

            s = get_object_or_404(Server, server_id=data['joined']['server'])
            s.members.add(member)

        if 'leaves' in data:
            member = get_object_or_404(Member, id=data['leaves']['id'])
            s = get_object_or_404(Server, server_id=data['leaves']['server'])
            s.members.remove(member)

        return HttpResponse('')

class ban(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, server_id):
        data = request.POST

        server = Server.objects.get(server_id=server_id)

        Ban(
            server = server,
            type   = data['type'],
            value  = data['value']
        ).save()

        Update(
            server   = server,
            type     = 'ban',
            ban_type = data['type'],
            value    = data['value']
        ).save()

        return redirect('servers:info', server_id=server_id)
