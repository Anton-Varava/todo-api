from abc import ABCMeta

from rest_framework import serializers
from .models import TodoItem, Board, User
# from .views import count_board_todos


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'


class BoardDetailSerializer(serializers.ModelSerializer):
    board_todos = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Board
        fields = '__all__'
        ordering = ['user', 'id', 'name', 'board_todos']

    def get_board_todos(self, obj):
        board_todo = TodoItem.objects.filter(board=obj)
        serializer = TodoItemSerializer(board_todo, many=True)
        return serializer.data


class BoardListSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = '__all__'

    @staticmethod
    def get_todo_count(obj):
        todo_count = TodoItem.objects.filter(board=obj).count()
        return todo_count


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
