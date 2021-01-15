# Generated by Django 3.1.5 on 2021-01-13 17:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customuser_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='leaders', to=settings.AUTH_USER_MODEL),
        ),
    ]