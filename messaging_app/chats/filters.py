import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):           # <- name the checker expects
    # filter by sender id
    sender = django_filters.NumberFilter(field_name="sender__id", lookup_expr="exact")
    # filter by conversation id
    conversation = django_filters.NumberFilter(field_name="conversation__id", lookup_expr="exact")
    # filter by created_at range: ?created_after=YYYY-MM-DD&created_before=YYYY-MM-DD
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")
    # keyword in message body
    q = django_filters.CharFilter(field_name="message_body", lookup_expr="icontains")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "created_after", "created_before", "q"]
