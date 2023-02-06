# Generated by Django 4.1.3 on 2022-11-15 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0014_alter_userfollowing_follower"),
    ]

    operations = [
        migrations.AlterField(
            model_name="posts",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="poster",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="userfollowing",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="userfollowing",
            name="target",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="being_followed",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]