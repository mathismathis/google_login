from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import ChatRoom, UserChatRoom
from myapp.serializers import ChatRoomSerializer, UserSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .models import User
from rest_framework.permissions import AllowAny


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(token)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get('credential')

        google_response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={credential}')
        if google_response.status_code == 200:
            google_data = google_response.json()
            email = google_data.get('email')
            name = google_data.get('name')
            photo_url = google_data.get('photo_url')

            try:
                user = User.objects.get(email=email)
                user.google_credential = credential
                user.save()
                user = authenticate(request, google_credential=credential)
                print(user)
                login(request, user)
                print(request.user, "authenticated")
            except User.DoesNotExist:
                user = User.objects.create(email=email, google_credential=credential, name=name, photo_url=photo_url)
                user = authenticate(request, google_credential=credential)
                login(request, user)
                print(request.user, "authenticated")

            user_data = {
                'email': user.email,
                'name': user.name,
                'photo_url': user.photo_url,
                'session_data': request.session,
            }

            refresh = RefreshToken.for_user(user)
            print(
                {'success': True, 'user': user_data, 'refresh': str(refresh), 'access': str(refresh.access_token)})
            return Response(
                {'success': True, 'user': user_data, 'refresh': str(refresh), 'access': str(refresh.access_token)})

        return Response({'success': False, 'message': 'Invalid Credential'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_chat_room(request, format=None):
    serializer = ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        chat_room = serializer.save()
        user_chat_room = UserChatRoom.objects.create(user=request.user, chat_room=chat_room)
        return JsonResponse({'room_id': chat_room.id})
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_chat_rooms(request, format=None):
    chat_rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        pass


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def all_user_list(request, format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
