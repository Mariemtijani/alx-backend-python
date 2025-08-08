from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# /api/conversations/…
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# /api/conversations/{conversation_pk}/messages/…
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + conversations_router.urls
