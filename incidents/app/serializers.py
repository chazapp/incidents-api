from django.contrib.auth.models import User, Group
from rest_framework import serializers, request

from incidents.app.models import Incident

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class IncidentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=True, max_length=500)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(required=True, max_length=100)
    severity = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Incident` instance, given the validated data.
        """
        return Incident.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Incident` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.severity = validated_data.get('severity', instance.severity)
        instance.save()
        return instance
