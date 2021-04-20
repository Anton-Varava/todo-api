from django.urls import path
from . import views

urlpatterns = [
    path('reminder-create', views.create_reminder, name='create-reminder'),
    path('reminder-list', views.list_user_reminders, name='reminder-list'),
    path('reminder-delete/<str:pk>', views.delete_reminder, name='delete-reminder')
]