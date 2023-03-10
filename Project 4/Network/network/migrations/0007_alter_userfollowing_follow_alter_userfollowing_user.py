# Generated by Django 4.1.3 on 2022-11-15 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0006_remove_userfollowing_following_userfollowing_follow"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfollowing",
            name="follow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="userfollowing",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
