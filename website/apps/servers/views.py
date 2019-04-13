from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
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

        print(request.user.is_superuser)
        print(request.user in server.moderators.all())
        print(request.user in server.admins.all())

        if not request.user.is_superuser and not request.user in server.moderators.all() and not request.user in server.admins.all():
            raise Http404('Not found')

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

        if not request.user.is_superuser and not request.user in server.moderators.all() and not request.user in server.admins.all():
            raise Http404('Not found')

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
                if request.user.is_superuser or request.user in server.admins.all():
                    server.moderators.add(user.user)
                else:
                    raise Http404('Not found')
            elif type[1] == 'admin':
                if request.user.is_superuser:
                    server.admins.add(user.user)
                else:
                    raise Http404('Not found')

            server.save()
        elif type[0] == 'domain':
            domain = EmailDomain(domain=value)
            domain.save()

            server.emails_domains.add(domain)
            server.save()

            Update(
                server   = server,
                type     = 'config',
            ).save()
        elif type[0] == 'channel':
            if not request.user.is_superuser or not request.user in server.admins.all():
                raise Http404('Not found')

            server.channel_admin   = request.POST.get('admin', 0)
            server.channel_logs    = request.POST.get('logs', 0)
            server.channel_request = request.POST.get('request', 0)

            server.save()

            Update(
                server   = server,
                type     = 'config',
            ).save()

        return redirect('servers:info', pk=pk)

class list(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        servers = Server.objects.all()

        if not request.user.is_superuser:
            for server in servers:
                if not request.user in server.moderators and not request.user in server.admins:
                    servers = servers.exclude(pk=server.pk)

        context = {
            'servers': servers
        }

        return render(request, "servers/list.html", context)

class ban(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, pk):
        server = get_object_or_404(Server, pk=pk)

        if not request.user.is_superuser and not request.user in server.moderators.all() and not request.user in server.admins.all():
            raise Http404('Not found')

        data = request.POST

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
    @method_decorator(staff_member_required)
    def get(self, request, pk):
        rank = get_object_or_404(Rank, pk=pk)

        server = rank.server

        if not request.user.is_superuser and not request.user in server.moderators.all() and not request.user in server.admins.all():
            raise Http404('Not found')

        Update(
            server   = server,
            type     = 'config',
        ).save()

        rank.delete()

        return redirect('servers:info', pk=server.id)

class deladmin(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, pk, user):
        if not request.user.is_superuser:
            raise Http404('Not found')

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
    @method_decorator(staff_member_required)
    def get(self, request, pk, user):
        server = get_object_or_404(Server, pk=pk)

        if not request.user.is_superuser and not request.user in server.admins.all():
            raise Http404('Not found')

        try:
            user = get_user_model().objects.get(pk=user)
        except get_user_model().DoesNotExist:
            return redirect('servers:info', pk=pk)

        server.moderators.remove(user)
        server.save()

        return redirect('servers:info', pk=pk)

class deldomain(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, pk, dpk):
        domain = get_object_or_404(EmailDomain, pk=dpk)
        server = get_object_or_404(Server, pk=pk)

        if not request.user.is_superuser and not request.user in server.admins.all():
            raise Http404('Not found')

        Update(
            server   = server,
            type     = 'config',
        ).save()

        domain.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class activate(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, pk):
        if not request.user.is_superuser:
            raise Http404('Nope')

        server = get_object_or_404(Server, pk=pk)
        server.is_active = True
        server.save()

        return redirect('servers:info', pk=pk)

class deactivate(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, pk):
        if not request.user.is_superuser:
            raise Http404('Nope')

        server = get_object_or_404(Server, pk=pk)
        server.is_active = False
        server.save()

        return redirect('servers:info', pk=pk)
