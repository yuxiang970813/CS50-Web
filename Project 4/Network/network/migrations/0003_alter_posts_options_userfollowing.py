# Generated by Django 4.1.3 on 2022-11-14 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_posts"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="posts",
            options={"ordering": ["-created_time"]},
        ),
        migrations.CreateModel(
            name="UserFollowing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True, related_name="follow", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
