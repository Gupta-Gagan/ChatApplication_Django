from django.db import models
from django.conf import settings


class Conversation(models.Model):

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_group = models.BooleanField(default=False)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ConversationParticipant',
        related_name='conversations'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_conversations'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversations"

    def __str__(self):
        if self.is_group:
            return self.name

        return f"Conversation {self.id}"


class ConversationParticipant(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "conversation_participants"

        unique_together = ['conversation', 'user']

    def __str__(self):
        return f"{self.user.email} in {self.conversation.id}"


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "messages"

        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.email}"