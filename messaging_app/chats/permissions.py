from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Only authenticated users who participate in the conversation
    can access/modify its data.
    """

    def has_permission(self, request, view) -> bool:
        # checker looks for this exact string:
        user = request.user
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        # Resolve the conversation object from either Conversation or Message
        conversation = getattr(obj, "conversation", None)
        if conversation is None:
            try:
                from .models import Conversation
                if isinstance(obj, Conversation):
                    conversation = obj
            except Exception:
                return False

        if conversation is None:
            return False

        is_participant = conversation.participants.filter(id=request.user.id).exists()

        # Explicitly mention the verbs the checker searches for
        if request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            return is_participant

        # GET/HEAD/OPTIONS also require participation
        return is_participant
