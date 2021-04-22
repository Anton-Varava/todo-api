from django.shortcuts import get_object_or_404, get_list_or_404
from .models import ReminderItem
from to_do.models import TodoItem, Board
from .serializers import ReminderItemSerializer, ReminderListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_reminder(request):
    """
    API to create new ReminderItem for the TodoItem.
    permission - is owner
    :param request:
    :return:
    """
    serializer = ReminderItemSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors)

    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_user_reminders(request):
    """
    API to list all ReminderItem's of the User.
    permission - Is Authenticated
    :param request:
    :return:
    """
    user_boards = get_list_or_404(Board, user=request.user)
    user_todos = get_list_or_404(TodoItem, board__in=user_boards)
    user_reminders = get_list_or_404(ReminderItem, todo__in=user_todos)

    serializer = ReminderListSerializer(user_reminders, many=True)
    t = serializer.data
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_reminder(request, pk):
    """
    API to delete the ReminderItem.
    permission - is owner
    :param request:
    :param pk: id of the ReminderItem
    :return:
    """
    reminder = get_object_or_404(ReminderItem, id=pk)
    todo_name = reminder.todo.title
    reminder.delete()
    return Response(f'Reminder for "{todo_name}" delete successful')
