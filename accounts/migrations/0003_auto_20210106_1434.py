# Generated by Django 3.1.5 on 2021-01-06 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(default='No bio entered', max_length=250),
        ),
    ]
