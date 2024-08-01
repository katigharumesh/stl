# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Users

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(email=username)
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(phone_number=username)
                except Users.DoesNotExist:
                    return None

        if user.check_password(password):
            return user
        return None
