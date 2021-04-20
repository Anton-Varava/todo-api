from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from to_do.models import TodoItem
from .serializers import ReminderItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_reminder(request):
    serializer = ReminderItemSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors)

    serializer.save()
    return Response(serializer.data)


