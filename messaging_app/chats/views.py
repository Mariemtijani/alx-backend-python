from rest_framework import viewsets, status, filters
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend   # <- needed

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username", "participants__email"]
    ordering_fields = ["id", "created_at"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conv = serializer.save()
        conv.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter                     # <- hook in MessageFilter
    search_fields = ["message_body", "sender__username"]
    ordering_fields = ["id", "created_at"]
    pagination_class = StandardResultsSetPagination     # <- 20 per page

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related("conversation").distinct()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        if not conversation.participants.filter(id=self.request.user.id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=HTTP_403_FORBIDDEN,
            )
        serializer.save(sender=self.request.user, conversation=conversation)
