
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('sentiment', '0007_create_stock_sector_table'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW sentiment_industrysector_summary
            AS
            SELECT row_number() OVER ()                                AS id,
                   avg(sentiment_tweet.sentiment)                      AS avg_sentiment,
                   date_trunc('day'::text, sentiment_tweet.created_at) AS date,
                   stock.sector_id
            FROM (sentiment_tweet
                     JOIN sentiment_tweet_stocks tweet_stocks ON ((sentiment_tweet.id = tweet_stocks.tweet_id))
                     JOIN sentiment_stock stock on tweet_stocks.stock_id = stock.id)
            GROUP BY date, stock.sector_id
            ORDER BY date;
            """,
            "DROP VIEW sentiment_industrysector_summary;"
        )
    ]
