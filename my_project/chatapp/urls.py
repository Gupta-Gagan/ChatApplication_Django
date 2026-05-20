from django.urls import path

from .views import (
    ConversationListCreateView,
    ConversationDetailView,
    MessageListView,
    MarkMessagesReadView
)

urlpatterns = [

    path(
        'conversations/',ConversationListCreateView.as_view(),name='conversation-list-create'
    ),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'
    ),

    path(
        'conversations/<int:conversation_id>/messages/',
        MessageListView.as_view(),
        name='message-list'
    ),

    path(
        'conversations/<int:conversation_id>/read/',
        MarkMessagesReadView.as_view(),
        name='mark-messages-read'
    ),
]