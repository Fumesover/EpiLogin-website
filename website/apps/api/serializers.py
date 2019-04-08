from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response

from website.apps.groups.models import Group, Ban, Update
from website.apps.members.models import Member
from website.apps.servers.models import Server, Rank, EmailDomain

class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = '__all__'

class EmailDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailDomain
        fields = '__all__'

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'

class ServerSerializer(serializers.ModelSerializer):
    rank_set       = RankSerializer(many=True, required=False)
    ban_set        = BanSerializer(many=True, required=False)
    emails_domains = EmailDomainSerializer(many=True, required=False)

    class Meta:
        model = Server
        fields = '__all__'

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
