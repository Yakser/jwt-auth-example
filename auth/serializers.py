from rest_framework import serializers


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username', required=True)
    password = serializers.CharField(label='Password', required=True)
