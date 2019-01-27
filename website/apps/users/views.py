from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from website.apps.servers.models import Server

class index(View):
    def get(self, request):
        return render(request, "users/index.html", {})

class home(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {
            'user': request.user,
            'user_extra': request.user.social_auth.get(provider="discord").extra_data,
            'servers': Server.objects.all()#.order_by('-date')
        }

        return render(request, "users/home.html", context)
