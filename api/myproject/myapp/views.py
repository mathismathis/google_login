from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import User
from django.contrib.auth import authenticate, login,logout
import requests

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import ChatRoom, UserChatRoom
from myapp.serializers import ChatRoomSerializer,UserSerializer

from django.contrib.sessions.models import Session
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from .models import User  # Make sure you import your User model correctly
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
                login(request, user)
                request.session['email'] = user.email
                print(request.user, "authenticated")
                print("Session Data:")
                for key, value in request.session.items():
                    print(f"{key}: {value}")
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
            print(user_data)
            
            return Response({'success': True, 'user': user_data})
        
        return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)
    
    




@api_view(['POST'])
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
   

    def get(self, request):
        print(request.user)
        logout(request)
        print("success")
        return Response({'success': True})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)  
    return Response(serializer.data)
