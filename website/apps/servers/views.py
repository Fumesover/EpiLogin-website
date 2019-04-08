from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model
import json

from website.apps.servers.models import Server, Rank, EmailDomain
from website.apps.members.models import Member
from website.apps.groups.models  import Group, Ban, Update

class info(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, pk):
        server = get_object_or_404(Server, pk=pk)

        bans = {
            'users':  Ban.objects.filter(server=server, type='user'),
            'groups': Ban.objects.filter(server=server, type='group'),
            'emails': Ban.objects.filter(server=server, type='email'),
        }

        ranks = {
            'confirmed': Rank.objects.filter(server=server, type='confirmed'),
            'classic': Rank.objects.filter(server=server, type='classic'),
            'banned': Rank.objects.filter(server=server, type='banned'),
        }

        context = {
            'server': server,
            'bans': bans,
            'ranks': ranks,
        }

        return render(request, "servers/info.html", context)

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)
        type = request.POST.get('type', '').split('-')
        value = request.POST.get('value', '')
        rank = request.POST.get('rank', '')

        if type[0] == 'ban':
            Ban(
                server = server,
                type   = type[1],
                value  = value
            ).save()

            Update(
                server   = server,
                type     = 'ban',
                ban_type = type[1],
                value    = value
            ).save()
        elif type[0] == 'role':
            Rank(
                server     = server,
                type       = type[1],
                name       = rank,
                discord_id = value
            ).save()

            Update(
                server   = server,
                type     = 'config',
                value    = value
            ).save()
        elif type[0] == 'serv':
            try:
                user = UserSocialAuth.objects.get(provider='discord', uid=value)
            except UserSocialAuth.DoesNotExist:
                return redirect('servers:info', pk=pk)

            if type[1] == 'mod':
                server.moderators.add(user.user)
            elif type[1] == 'admin':
                server.admins.add(user.user)
        elif type[0] == 'domain':
            domain = EmailDomain(domain=value)
            domain.save()

            server.emails_domains.add(domain)
            server.save()

            Update(
                server   = server,
                type     = 'config',
                value    = value
            ).save()

        return redirect('servers:info', pk=pk)

class list(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        context = {
            'servers': Server.objects.all()
        }

        return render(request, "servers/list.html", context)

class ban(View):
    @method_decorator(login_required)
    @method_decorator(permission_required('groups.add_ban'))
    def post(self, request, pk):
        data = request.POST

        server = get_object_or_404(Server, pk=pk)

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

        return redirect('servers:info', pk=pk)

class deleterank(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        rank = get_object_or_404(Rank, pk=pk)

        server_id = rank.server.id

        Update(
            server   = server_id,
            type     = 'config',
            value    = value
        ).save()

        rank.delete()

        return redirect('servers:info', pk=server_id)

class deladmin(View):
    @method_decorator(login_required)
    def get(self, request, pk, user):
        server = get_object_or_404(Server, pk=pk)

        try:
            user = get_user_model().objects.get(pk=user)
        except get_user_model().DoesNotExist:
            return redirect('servers:info', pk=pk)

        server.admins.remove(user)
        server.save()

        return redirect('servers:info', pk=pk)

class delmod(View):
    @method_decorator(login_required)
    def get(self, request, pk, user):
        server = get_object_or_404(Server, pk=pk)

        try:
            user = get_user_model().objects.get(pk=user)
        except get_user_model().DoesNotExist:
            return redirect('servers:info', pk=pk)

        server.moderators.remove(user)
        server.save()

        return redirect('servers:info', pk=pk)

class deldomain(View):
    @method_decorator(login_required)
    def get(self, request, pk, dpk):
        domain = get_object_or_404(EmailDomain, pk=dpk)
        server = get_object_or_404(Server, pk=pk)

        Update(
            server   = server,
            type     = 'config',
        ).save()

        domain.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
