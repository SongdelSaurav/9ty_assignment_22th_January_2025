from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat_project.chat import models
from chat_project.chat.models import CustomUser, Message
from serializers import UserSerializer, MessageSerializer 

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver_id):
        messages = Message.objects.filter(
            (models.Q(sender=request.user, receiver_id=receiver_id) |
             models.Q(sender_id=receiver_id, receiver=request.user))
        )
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
