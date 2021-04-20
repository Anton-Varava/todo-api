from rest_framework import serializers
from .models import ReminderItem, TodoItem
from django.shortcuts import get_object_or_404


class ReminderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReminderItem
        fields = '__all__'

    def create(self, validated_data):
        reminder = ReminderItem(
            email=validated_data['email'],
            text=validated_data['text'],
            reminder_date=validated_data['reminder_date'],
            todo=validated_data['todo']
        )
        reminder.save()
        return reminder

