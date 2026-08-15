from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class EmailAuthenticationBackend(BaseBackend):

    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = User.objects.get(email = username)

            if password is not None and user.check_password(password):
                return user
            return None

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None 


    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return