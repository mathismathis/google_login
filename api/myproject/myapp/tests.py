from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from myapp.models import ChatRoom
from myapp.serializers import ChatRoomSerializer, UserSerializer

class GoogleLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.credentials = {'credential': 'your_google_credential_here'}

    def test_google_login_success(self):
        response = self.client.post('api/login/', data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue('user' in response.data)
        # Add more assertions to check the response data

    def test_google_login_failure(self):
        # Test with invalid Google credential
        invalid_credentials = {'credential': 'invalid_google_credential'}
        response = self.client.post('/api/google-login/', data=invalid_credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

# class CreateChatRoomViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         self.chat_room_data = {'name': 'Test Chat Room'}
#
#     def test_create_chat_room(self):
#         response = self.client.post('/api/create-chat-room/', data=self.chat_room_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue('room_id' in response.data)
#         # Add more assertions to check the response data
#
#     def test_create_chat_room_invalid_data(self):
#         # Test with invalid data
#         invalid_data = {'name': ''}
#         response = self.client.post('/api/create-chat-room/', data=invalid_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # Add more assertions to check the response data


# class ListChatRoomsViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         self.chat_room1 = ChatRoom.objects.create(name='Chat Room 1')
#         self.chat_room2 = ChatRoom.objects.create(name='Chat Room 2')
#
#     def test_list_chat_rooms(self):
#         response = self.client.get('/api/list-chat-rooms/')
#
#         # Add debugging statements
#         print(response.status_code)
#         print(response.content)  # You can print the response content to inspect it
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#         # Add more assertions to check the response data
#

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        response = self.client.post('api/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AllUserListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_all_user_list(self):
        response = self.client.get('api/user_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to check the response data
