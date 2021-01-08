from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=250, default="No bio entered")
    profile_picture_link = models.TextField(
        max_length=250,
        default="https://upload.wikimedia.org/wikipedia/en/1/1b/NPC_wojak_meme.png",
    )
