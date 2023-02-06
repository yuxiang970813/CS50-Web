# Generated by Django 4.1.2 on 2022-11-05 16:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionwatchlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='buy_later', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='AuctionWatchlist',
        ),
    ]
