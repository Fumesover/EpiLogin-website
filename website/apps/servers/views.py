from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
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
