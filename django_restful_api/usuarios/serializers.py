from django.contrib.auth.models import Group, User
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = serializers.CharField(write_only=True)

    def validate_group(self, group_name):
        try:
            group = Group.objects.filter(name=group_name)
            if not group.exists():
                raise serializers.ValidationError("Este grupo não existe.")
            return group
        except:
            raise serializers.ValidationError("Este grupo não existe.")

    def create(self, validated_data):
        try:
            groups_data = validated_data['group']
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.groups.set(groups_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'email', 'group']
