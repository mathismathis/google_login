from django.contrib.auth.backends import ModelBackend
from myapp.models import User  

class GoogleOAuthBackend(ModelBackend):
    def authenticate(self, request, google_credential=None):
       
        try:
            user = User.objects.get(google_credential=google_credential)
            return user
        except User.DoesNotExist:
            return None
