from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .serializers import *
from .permissions import *
from website.apps.groups.models import Group, Ban, Update
from website.apps.members.models import Member
from website.apps.servers.models import Server, Rank

class UpdateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('type', 'ban_type', 'server', 'email')

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperUserOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('email', 'group')

class RankViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = Rank.objects.all()
    serializer_class = RankSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:
            servers = (user.admin.all() | user.moderator.all()).distinct()
            ranks = Rank.objects.none()
            for server in servers:
                ranks = ranks | server.rank_set.all()
            return ranks.distinct()
        else:
            return Rank.objects.all()

class ServerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:
            return (user.admin.all() | user.moderator.all()).distinct()
        else:
            return Server.objects.all()

class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('email', 'servers', 'name')

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:
            servers = (user.admin.all() | user.moderator.all()).distinct()
            members = Member.objects.none()
            for server in servers:
                members = members | server.member_set.all()
            return members.distinct()
        else:
            return Member.objects.all()

#    @action(detail=True, methods=['post'])
#    def certify(self, request, pk=None):
#        email = request.data.get('email')
#
#        if email:
#            member, _ = Member.objects.get_or_create({'pk': pk})
#            member.email = email
#            member.hash = ''
#            member.save()
#            return Response({'status': 'User certified'})
#        else:
#            return Response({'status': 'Invalid request'}, status=400)

    @action(detail=True, methods=['post', 'delete'], permission_classes=(IsSuperUser,))
    def server(self, request, pk=None):
        member = get_object_or_404(Member, pk=pk)

        server_id = request.data.get('id')

        if server_id:
            try:
                server = Server.objects.get(pk=server_id)
            except Member.DoesNotExist:
                raise NotFound('Member not found.', code=405)

            if request.method == 'POST':
                member.servers.add(server)
                member.save()
                return Response({'status': 'Server added'})
            elif request.method == 'DELETE':
                member.servers.remove(server)
                member.save()
                return Response({'status': 'Server removed'})
        else:
            return Response({'status': 'Invalid request'}, status=400)
