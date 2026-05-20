from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accountsapp.models import CustomUser
from .serializers import MessageSerializer
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    CreateConversationSerializer
)


class ConversationListCreateView(
    generics.ListCreateAPIView
):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Conversation.objects.filter(
            participants=self.request.user
        ).distinct()

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateConversationSerializer

        return ConversationSerializer
    
    
class ConversationDetailView(generics.RetrieveAPIView):

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Conversation.objects.filter(
            participants=self.request.user
        )


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_conversation(self):
        conversation_id = self.kwargs.get("conversation_id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation does not exist")

        # Check if user is participant
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation")

        return conversation

    def get_queryset(self):
        conversation = self.get_conversation()

        return Message.objects.filter(
            conversation=conversation
        ).order_by("created_at")

    def perform_create(self, serializer):
        conversation = self.get_conversation()

        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
        
        
class MarkMessagesReadView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):

        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=request.user
            )

        except Conversation.DoesNotExist:

            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        unread_messages = Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(
            sender=request.user
        )

        updated_count = unread_messages.update(
            is_read=True
        )

        return Response(
            {
                "message": "Messages marked as read",
                "updated_count": updated_count
            },
            status=status.HTTP_200_OK
        )
        
        
class AddParticipantView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):

        user_id = request.data.get("user_id")

        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                is_group=True,
                participants=request.user
            )

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # check admin
        is_admin = conversation.conversationparticipant_set.filter(
            user=request.user,
            is_admin=True
        ).exists()

        if not is_admin:
            return Response(
                {"error": "Only admins can add members"},
                status=status.HTTP_403_FORBIDDEN
            )

        # check user exists
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # already member check
        if conversation.participants.filter(id=user.id).exists():
            return Response(
                {"error": "User already in group"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation.participants.add(user)

        return Response(
            {"message": "User added successfully"},
            status=status.HTTP_200_OK
        )
        
        
class RemoveParticipantView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):

        user_id = request.data.get("user_id")

        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                is_group=True,
                participants=request.user
            )

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # allow admin OR self leave
        is_admin = conversation.conversationparticipant_set.filter(
            user=request.user,
            is_admin=True
        ).exists()

        if request.user.id != user_id and not is_admin:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        conversation.participants.remove(user)

        return Response(
            {"message": "User removed successfully"},
            status=status.HTTP_200_OK
        )