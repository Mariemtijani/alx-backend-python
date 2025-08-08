from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Grants access only if the request.user participates in the target conversation.
    Works for both Conversation and Message objects.
    """

    message = "You are not a participant in this conversation."

    def _user_in_conversation(self, user, conversation) -> bool:
        return conversation.participants.filter(id=user.id).exists()

    def has_object_permission(self, request, view, obj) -> bool:
        # Conversation object
        try:
            from .models import Conversation  # local import to avoid cycles
            if isinstance(obj, Conversation):
                return self._user_in_conversation(request.user, obj)
        except Exception:
            pass

        # Message object (traverse to its conversation)
        try:
            conversation = getattr(obj, "conversation", None)
            if conversation is not None:
                return self._user_in_conversation(request.user, conversation)
        except Exception:
            pass

        return False
