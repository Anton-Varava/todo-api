from django.shortcuts import get_object_or_404, get_list_or_404
from .models import TodoItem, Board
from .serializers import TodoItemSerializer, BoardDetailSerializer, UserSerializer, BoardListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


def is_owner(user, obj):
    if user == obj.user:
        return True
    return False


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        response_data = serializer.errors
    else:
        serializer.save()
        response_data = serializer.data
    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_board(request):
    data = request.data
    data['user'] = request.user.id
    serializer = BoardDetailSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def board_list(request):
    boards = Board.objects.filter(user=request.user)
    serializer = BoardListSerializer(boards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_board_detail(request, pk):
    board = get_object_or_404(Board, id=pk)
    serializer = BoardDetailSerializer(board)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_board(request):
    try:
        board_id = int(request.data['id'])
    except KeyError as err:
        return Response(f'{err} is not define')
    except ValueError as err:
        return Response(str(err))
    board = Board.objects.get(id=board_id)
    if is_owner(user=request.user, obj=board.user):
        board_name = board.name
        board.delete()

        return Response(f"Board '{board_name}' delete successfully")
    else:
        return Response("You don't have permission to delete this board")


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def change_name_board(request):
    try:
        board_id = int(request.data['id'])
        new_name = request.data['name']
    except KeyError as err:
        return Response(f'{err} is not define')
    except ValueError as err:
        return Response(str(err))
    board = get_object_or_404(Board, id=board_id)
    if not is_owner(request.user, board):
        return Response('You don\'t have permission to change this board')
    new_data = {'name': new_name}
    serializer = BoardDetailSerializer(board, data=new_data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_todo_item(request):
    board = Board.objects.get(id=request.data['board'])
    if not is_owner(request.user, board):
        return Response(f"You don't have permission to create ToDO item to board - {board.id}")

    serializer = TodoItemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_todo(request):

    try:
        board_id = int(request.data['board'])
    except KeyError as err:
        return Response(f'{err} is not define')
    except ValueError as err:
        return Response(str(err))

    board = get_object_or_404(Board, id=board_id)

    if not is_owner(request.user, board):
        return Response('You don\'t have permission to this board')
    if 'is_done' in request.data:
        board_todos = get_list_or_404(TodoItem, board=board, isDone=request.data['is_done'])
    else:
        board_todos = get_list_or_404(TodoItem, board=board)

    serializer = TodoItemSerializer(board_todos, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def edit_todo(request, pk):
    new_data = {}
    if 'title' in request.data:
        new_title = request.data['title']
        new_data['title'] = new_title
    if 'is_done' in request.data:
        new_status = request.data['is_done']
        new_data['isDone'] = new_status
    todo = get_object_or_404(TodoItem, id=pk)
    board = get_object_or_404(Board, id=todo.board.id)
    if not is_owner(request.user, board):
        return Response('You don\'t have permission to this board')

    serializer = BoardDetailSerializer(board, data=new_data, partial=True)
    serializer = TodoItemSerializer(todo, data=new_data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_todo(request):
    try:
        todo_id = int(request.data['id'])
    except KeyError as err:
        return Response(f'{err} is not define')
    except ValueError as err:
        return Response(str(err))
    todo_item = get_object_or_404(TodoItem, id=todo_id)
    todo_item_name = todo_item.title
    if not is_owner(request.user, todo_item.board):
        return Response('You don\'t have permission to this item')
    todo_item.delete()
    return Response(f'"{todo_item_name}" delete successfully')


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def board_list_all(request):
    boards_all = Board.objects.all()
    serializer = BoardDetailSerializer(boards_all, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def todo_list_all(request):
    todos_all = TodoItem.objects.all()
    serializer = TodoItemSerializer(todos_all, many=True)
    return Response(serializer.data)




