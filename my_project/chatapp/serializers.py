from rest_framework import serializers
from accountsapp.serializers import UserProfileSerializer
from my_project.accountsapp.models import CustomUser
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):

    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Message

        fields = [
            'id',
            'conversation',
            'sender',
            'sender_email',
            'content',
            'is_read',
            'created_at'
        ]

        read_only_fields = [
            'sender',
            'conversation'
        ]

    def get_sender_email(self, obj):

        return obj.sender.email
    
    
    
class ConversationSerializer(serializers.ModelSerializer):

    participants = UserProfileSerializer(
        many=True,
        read_only=True
    )

    last_message = serializers.SerializerMethodField()

    unread_count = serializers.SerializerMethodField()
    
    participant_count = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = Conversation

        fields = [
            'id',
            'name',
            'is_group',
            'participants',
            'created_by',
            'last_message',
            'unread_count',
            'created_at'
        ]

    def get_last_message(self, obj):

        last_message = obj.messages.last()

        if last_message:
            return MessageSerializer(last_message).data

        return None

    def get_unread_count(self, obj):

        request = self.context.get('request')

        user = request.user

        return obj.messages.filter(
            is_read=False
        ).exclude(
            sender=user
        ).count()
        
        
class CreateConversationSerializer(serializers.Serializer):

    participant_id = serializers.IntegerField(
        required=False
    )

    name = serializers.CharField(
        required=False
    )

    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    is_group = serializers.BooleanField()

    def validate(self, attrs):

        is_group = attrs.get('is_group')

        request = self.context.get('request')

        current_user = request.user

        # One-to-one chat validation
        if not is_group:

            participant_id = attrs.get('participant_id')

            if not participant_id:
                raise serializers.ValidationError(
                    "participant_id is required"
                )

            # Check user exists
            if not CustomUser.objects.filter(
                id=participant_id
            ).exists():

                raise serializers.ValidationError(
                    "Participant does not exist"
                )

            # Check if conversation already exists
            existing_conversations = Conversation.objects.filter(
                is_group=False,
                participants=current_user
            )

            for conversation in existing_conversations:

                participants = conversation.participants.all()

                if (
                    participants.count() == 2 and
                    participants.filter(id=participant_id).exists()
                ):
                    raise serializers.ValidationError(
                        "Conversation already exists"
                    )

        # Group chat validation
        else:

            participant_ids = attrs.get('participant_ids')

            name = attrs.get('name')

            if not name:
                raise serializers.ValidationError(
                    "Group name is required"
                )

            if not participant_ids:
                raise serializers.ValidationError(
                    "participant_ids are required"
                )

            users_count = CustomUser.objects.filter(
                id__in=participant_ids
            ).count()

            if users_count != len(participant_ids):
                raise serializers.ValidationError(
                    "Some participants do not exist"
                )

        return attrs