from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('board-create', views.create_board, name='create-board'),
    path('board-list', views.board_list, name='board-list'),
    path('board-delete', views.delete_board, name='board-delete'),
    path('board-change', views.change_name_board, name='board-change'),
    path('board/<str:pk>', views.get_board_detail, name='board-detail'),
    path('api-token-auth', obtain_auth_token, name='api-token-auth'),
    path('todo-create', views.create_todo_item, name='todo-create'),
    path('todo-list', views.list_todo, name='todo-list'),
    path('todo-delete', views.delete_todo, name='todo-delete'),
    path('todo/<str:pk>/edit', views.edit_todo, name='edit-todo'),
    path('sign-up', views.create_user, name='create-user'),
    path('todo-list-all', views.todo_list_all, name='todo-list-all'),
    path('board-list-all', views.board_list_all, name='board-list-all')
]
