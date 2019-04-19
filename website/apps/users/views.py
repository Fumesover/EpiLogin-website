from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseForbidden
import sys

from website.apps.members.models import Member
from website.apps.servers.models import Server
from website.apps.groups.models  import Group, Ban, Update

class index(View):
    def get(self, request):
        return render(request, "users/index.html", {})

class home(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        context = {
            'user': request.user,
        }

        return render(request, "users/home.html", context)

class certify(View):
    @method_decorator(login_required)
    def get(self, request):
        print(request.user.email)
        login, domain = request.user.email.split('@')
        if domain != 'epita.fr':
            logout(request)
            return redirect('/login/?next=/certify/?token=' + request.GET['token'])

        if 'token' in request.GET:
            try:
                member = Member.objects.get(hash=request.GET['token'])
            except Member.DoesNotExist:
                return None # TODO: HANDLE ERROR

            member.hash = ''
            member.login = login
            member.save()

            Update(
                type='certify',
                login=login,
                value=member.id,
            ).save()
            return redirect('certify')

        return render(request, 'registration/confirm.html')
