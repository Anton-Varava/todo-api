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
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
