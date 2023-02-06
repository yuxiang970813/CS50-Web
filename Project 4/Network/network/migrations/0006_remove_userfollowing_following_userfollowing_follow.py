# Generated by Django 4.1.3 on 2022-11-14 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_remove_userfollowing_following_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userfollowing",
            name="following",
        ),
        migrations.AddField(
            model_name="userfollowing",
            name="follow",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follow",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
