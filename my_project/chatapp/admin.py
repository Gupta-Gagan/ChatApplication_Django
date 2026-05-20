from django.contrib import admin

from .models import (
    Conversation,
    ConversationParticipant,
    Message
)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'is_group',
        'created_by',
        'created_at'
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'is_group',
        'created_at'
    )


@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'conversation',
        'user',
        'is_admin',
        'joined_at'
    )

    list_filter = (
        'is_admin',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'conversation',
        'sender',
        'is_read',
        'created_at'
    )

    search_fields = (
        'content',
    )

    list_filter = (
        'is_read',
        'created_at'
    )