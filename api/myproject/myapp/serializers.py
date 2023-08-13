from rest_framework import serializers
from .models import ChatRoom, UserChatRoom,User

class UserChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatRoom
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserChatRoomSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
