# Generated by Django 3.1.5 on 2021-01-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210106_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture_link',
            field=models.TextField(default='data:image/png;base64,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', max_length=250),
        ),
    ]
