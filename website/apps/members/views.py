from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
import json

from website.apps.members.models import Member
from website.apps.servers.models import Server
from website.apps.groups.models  import Group, Ban, Update

class profile(View):
    @method_decorator(login_required)
    def get(self, request, id):
        member  = get_object_or_404(Member, id=id)
        servers = Server.objects.filter(members__in=[member])

        context = {
            'user': request.user,
            'user_extra': request.user.social_auth.get(provider="discord").extra_data,
            'profile': member,
            'servers': servers,
            'groups': Group.objects.filter(login=member.login),
        }

        return render(request, "users/profile.html", context)

class addgroup(View):
    @method_decorator(login_required)
    def post(self, request, id):
        member = get_object_or_404(Member, id=id)

        if member.login == '':
            return HttpResponseNotFound('User does not get a login')

        data = request.POST

        Group(
            login=member.login,
            group=data['value'],
        ).save()

        Update(
            type     = 'addgroup',
            login    = member.login,
            value    = data['value']
        ).save()

        return redirect('members:profile', id=id)
