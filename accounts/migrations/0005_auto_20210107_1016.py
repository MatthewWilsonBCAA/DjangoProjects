# Generated by Django 3.1.5 on 2021-01-07 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_profile_picture_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture_link',
            field=models.TextField(default='https://lh3.googleusercontent.com/proxy/QSgtl4IyCRgbj6yGyBM9Mqs_DMPmvS7LO5wqICSOcG9YCKQ8bn6n9RoQaQPN0zigsYK9JMOWzNRYH7t6-DRg-Hgor8DSjxcEGL3fatwotYlp9zW-38wyz9XuI54UlXp6ewSwSYsA8H6uh2wU9Sdkkug', max_length=250),
        ),
    ]
