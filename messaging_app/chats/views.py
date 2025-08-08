from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import (
    IsConversationParticipant,
    IsMessageSenderOrConversationParticipant,
)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]  # default; object checks below
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username", "participants__email"]
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        # Only conversations the current user participates in
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.save()  # create empty then set participants from serializer
        # make sure creator is participant (if not already provided)
        conversation.participants.add(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)  # enforce IsConversationParticipant if you add it globally
        return super().retrieve(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__username"]
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        # Messages that belong to conversations the user participates in
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related("conversation").distinct()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # guard: user must be in that conversation
        if not conversation.participants.filter(id=self.request.user.id).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
