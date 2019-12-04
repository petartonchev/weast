# Generated by Django 2.2.7 on 2019-11-26 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0005_create_stock_summary_view'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE or REPLACE view sentiment_stock_summary
                AS SELECT row_number() OVER ()           AS id,
                            avg(sentiment_tweet.sentiment) AS avg_sentiment,
                            sts.stock_id,
                            date_trunc('day', sentiment_tweet.created_at)     as date
                FROM (sentiment_tweet
                         JOIN sentiment_tweet_stocks sts ON ((sentiment_tweet.id = sts.tweet_id)))
                GROUP BY sts.stock_id, date
                ORDER BY date;
            """,
            """
            CREATE or REPLACE view sentiment_stock_summary
                AS SELECT row_number() OVER () as id,
                       AVG(sentiment) as avg_sentiment,
                       stock_id
                FROM sentiment_tweet
                INNER JOIN sentiment_tweet_stocks sts ON sentiment_tweet.id = sts.tweet_id
                WHERE sentiment_tweet.created_at >= now()::date
                GROUP BY stock_id;
            """,
        )
    ]