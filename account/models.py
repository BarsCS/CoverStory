from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 


class Follow(models.Model):

    user_from = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='rel_from')
    user_to = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='rel_to')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(fields=['user_from', 'user_to'], name='unique_user_follow')
        ]

    def __str__(self):
        return f'{self.user_from.user.username} follows {self.user_to.user.username}'


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default/default.png')
    name = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1024, blank=True)
    following = models.ManyToManyField('self', through=Follow, related_name='followers', symmetrical=False)

    class Meta:
        indexes = [models.Index(fields=['-name'])]

    def __str__(self):
        return f'Profile of @{ self.user.username }'

