from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=250, default="No bio entered")
    profile_picture_link = models.TextField(
        max_length=250,
        default="https://lh3.googleusercontent.com/proxy/QSgtl4IyCRgbj6yGyBM9Mqs_DMPmvS7LO5wqICSOcG9YCKQ8bn6n9RoQaQPN0zigsYK9JMOWzNRYH7t6-DRg-Hgor8DSjxcEGL3fatwotYlp9zW-38wyz9XuI54UlXp6ewSwSYsA8H6uh2wU9Sdkkug",
    )
