from django.db import models
from to_do.models import TodoItem


class ReminderItem(models.Model):
    email = models.EmailField(verbose_name='Email', max_length=50)
    text = models.CharField(verbose_name='Reminder Text', max_length=200)
    reminder_date = models.DateTimeField(verbose_name='Reminder Date')
    todo = models.ForeignKey(TodoItem, verbose_name='ToDo', on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated', auto_now=True)


    def __str__(self):
        return f"Todo '{self.todo.name}' remind!"

