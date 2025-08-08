from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username", "participants__email"]
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        # Only conversations where the user participates
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conv = serializer.save()
        # ensure creator is a participant
        conv.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__username"]
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        # Only messages in the user's conversations
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related("conversation").distinct()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # permission: must be a participant of this conversation
        if not conversation.participants.filter(id=self.request.user.id).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
