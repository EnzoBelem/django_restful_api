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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    group = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required= True)
    first_name = serializers.CharField(required= True)
    last_name = serializers.CharField(required= True)

    def validate_group(self, group_name):
        group = Group.objects.filter(name=group_name)
        if not group.exists():
            raise serializers.ValidationError("Este grupo não existe.")
        return group
        
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
            last_name=validated_data['last_name'],
        )
        user.groups.set(groups_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'group']


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    def validate_username(self, username):
        if not self.instance.username == username:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Este username não está disponivel.")
        return username

    def update(self, instance, validated_data):
        try:
            username = validated_data.get('username', instance.username)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.username = username
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'email']
        read_only_fields = ['id']
        