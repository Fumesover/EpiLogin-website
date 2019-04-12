from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
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

class list(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        context = {
            'members': Member.objects.all(),
        }

        return render(request, 'members/list.html', context)

class profile(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, id):
        member  = get_object_or_404(Member, id=id)

        context = {
            'member': member,
            'member_groups': Group.objects.filter(email=member.email),
        }

        if member.email:
            context['groups'] = Group.objects.filter(email=member.email)

        return render(request, "members/profile.html", context)

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, id):
        member = get_object_or_404(Member, id=id)
        member.email = request.POST.get('email', '')
        member.save()

        Update(
            type='certify',
            email=member.email,
            value=member.id,
        ).save()

        return redirect('members:profile', id=member.id)


class addgroup(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, id):
        member = get_object_or_404(Member, id=id)

        if member.email == '':
            return HttpResponseNotFound('User does not get an email')

        data = request.POST

        Group(
            email=member.email,
            group=data['group'],
        ).save()

        Update(
            type     = 'addgroup',
            email    = member.email,
            value    = data['group']
        ).save()

        return redirect('members:profile', id=id)

class delete(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, id):
        member = get_object_or_404(Member, id=id)

        member.delete()

        return redirect('members:list')
