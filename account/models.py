from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default/default.png')
    name = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1024, blank=True)

    class Meta:
        indexes = [models.Index(fields=['-name'])]

    def __str__(self):
        return f'Profile of @{ self.user.username }' 
