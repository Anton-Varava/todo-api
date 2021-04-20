from rest_framework import serializers
from .models import ReminderItem


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


class ReminderListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    todo = serializers.CharField()
    text = serializers.CharField()
    email = serializers.EmailField()
    # class Meta:
    #     model = ReminderItem
    #     fields = ('id', 'text', 'todo', 'reminder_date')

