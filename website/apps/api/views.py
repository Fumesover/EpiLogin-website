from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from .serializers import *
from website.apps.groups.models import Group, Ban, Update
from website.apps.members.models import Member
from website.apps.servers.models import Server

class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('login', 'group')


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('login', 'servers')

    @action(detail=True, methods=['post'])
    def certify(self, request, pk=None):
        login = request.data.get('login')

        if login:
            member, _ = Member.objects.get_or_create({'pk': pk})
            member.login = login
            member.hash = ''
            member.save()
            return Response({'status': 'User certified'})
        else:
            return Response({'status': 'Invalid request'}, status=400)

    @action(detail=True, methods=['post', 'delete'])
    def server(self, request, pk=None):
        server_id = request.data.get('id')

        if server_id and pk:
            member = Server.objects.get(pk=pk)

            try:
                member = Member.objects.get(pk=member_id)
            except Member.DoesNotExist:
                raise NotFound('Member not found.', code=405)

            if request.method == 'POST':
                server.members.add(member)
                server.save()
                return Response({'status': 'User added'})
            elif request.method == 'DELETE':
                server.members.remove(member)
                server.save()
                return Response({'status': 'User removed'})
        else:
            return Response({'status': 'Invalid request'}, status=400)
