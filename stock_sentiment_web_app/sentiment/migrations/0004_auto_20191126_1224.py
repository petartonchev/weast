# Generated by Django 2.2.7 on 2019-11-26 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0003_tweet_tweet_id'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tweet',
            constraint=models.UniqueConstraint(fields=('tweet_id',), name='unique-tweets'),
        ),
    ]
