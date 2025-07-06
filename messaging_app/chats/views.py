from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants')
        if not participants_ids:
            return Response({'error': 'participants list is required'}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants_ids)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({'error': 'conversation and message_body are required'}, status=400)

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=201)
