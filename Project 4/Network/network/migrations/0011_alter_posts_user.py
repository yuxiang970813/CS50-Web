# Generated by Django 4.1.3 on 2022-11-15 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0010_alter_userfollowing_target"),
    ]

    operations = [
        migrations.AlterField(
            model_name="posts",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]