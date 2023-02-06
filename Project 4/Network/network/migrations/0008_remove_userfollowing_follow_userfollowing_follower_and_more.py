# Generated by Django 4.1.3 on 2022-11-15 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0007_alter_userfollowing_follow_alter_userfollowing_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userfollowing",
            name="follow",
        ),
        migrations.AddField(
            model_name="userfollowing",
            name="follower",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="follower",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="userfollowing",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
