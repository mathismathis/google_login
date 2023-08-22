from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ChatRoom, UserChatRoom
from myapp.serializers import ChatRoomSerializer, UserSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .models import User
from rest_framework.permissions import AllowAny


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get('credential')

        google_response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={credential}')
        if google_response.status_code == 200:
            google_data = google_response.json()
            email = google_data.get('email')
            name = google_data.get('name')
            photo_url = google_data.get('picture')

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
def create_chat_room(request):
    serializer = ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        chat_room = serializer.save()
        user_chat_room = UserChatRoom.objects.create(user=request.user, chat_room=chat_room)
        return JsonResponse({'room_id': chat_room.id})
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data)


class LogoutView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        print(request.user)

        return Response({'success': True, 'message': 'Logout successful'})

@api_view(['GET'])
@permission_classes([AllowAny])
def all_user_list(request,format=None):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)