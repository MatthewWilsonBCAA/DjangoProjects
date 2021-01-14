from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model


# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=250, default="No bio entered")
    profile_picture_link = models.TextField(
        max_length=250,
        default="https://upload.wikimedia.org/wikipedia/en/1/1b/NPC_wojak_meme.png",
    )
    followers = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="leaders"
    )

    def total_votes(self):
        Vote = apps.get_model("blog", "Vote")
        return Vote.objects.filter(post__author__username=self.username).count()

    def total_followers(self):
        return self.followers.count()
