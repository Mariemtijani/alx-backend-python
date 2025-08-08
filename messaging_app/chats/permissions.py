from rest_framework import permissions
from .models import Conversation, Message

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only if the user participates in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        return False


class IsMessageSenderOrConversationParticipant(permissions.BasePermission):
    """
    Allow access to a message if the user is the sender or a participant
    of the parent conversation.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            if obj.sender_id == request.user.id:
                return True
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False
