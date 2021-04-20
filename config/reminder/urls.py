from django.urls import path
from . import views

urlpatterns = [
    path('reminder-create', views.create_reminder, name='create-reminder'),
]