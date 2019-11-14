db.createUser(
    {
        user: "moodstock",
        pwd: "debug",
        roles: [
            {
                role: "readWrite",
                db: 'moodstock_nosql_db'
            }
        ]
    }
)

// db.tweets.insertMany([
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c18"},
//         "text": "$ES_F #ES #es_f S&amp;P 500 Futures .. Hourly\nBroke neck line! https://t.co/PXX3FtJ6dW",
//         "created_at": {"$date": "2019-11-13T09:41:19Z"},
//         "user_name": "winner_trader",
//         "stock": ["$ES"],
//         "retweet_count": 1
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c19"},
//         "text": "Robotic Revolution watch-list from Yahoo.. (By market cap)\n$HON Honeywell International  $182\n$LMT Lockheed Martin… https://t.co/lHAdl04eOr",
//         "created_at": {"$date": "2019-11-13T06:17:06Z"},
//         "user_name": "winner_trader",
//         "stock": ["$HON", "$LMT"],
//         "retweet_count": 1
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1a"},
//         "text": "$TSLA Closed with bullish candle after late good headlines . Now levels raised . Stops for long became 340 . target… https://t.co/SVehy4d3SN",
//         "created_at": {"$date": "2019-11-13T06:07:06Z"},
//         "user_name": "winner_trader",
//         "stock": ["$TSLA"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1b"},
//         "text": "$ES_F #ES #es_f S&amp;P 500 Futures .. \nUpdate for Advanced Blocks pattern. #candlesticks #patterns\nShorts can start af… https://t.co/fUY9YKmQwV",
//         "created_at": {"$date": "2019-11-13T05:47:47Z"},
//         "user_name": "winner_trader",
//         "stock": ["$ES"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1c"},
//         "text": "#es_f $ES_F S&amp;P Futures $ES $SPX $SPY . \nOne of Bearish scenarios for $ES_F . \nGoals: \n2950 by end of Nov \n2895 by… https://t.co/Bp67K8e1Zv",
//         "created_at": {"$date": "2019-11-13T05:31:51Z"},
//         "user_name": "winner_trader",
//         "stock": ["$ES", "$ES", "$SPX", "$SPY", "$ES"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1d"},
//         "text": "$ROKU &amp; $FB Best performance for today",
//         "created_at": {"$date": "2019-11-12T20:02:34Z"},
//         "user_name": "winner_trader",
//         "stock": ["$ROKU", "$FB"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1e"},
//         "text": "It will be Game Over if $SPX $SPY #ES_F $ES_F Closed in Red!!",
//         "created_at": {"$date": "2019-11-12T19:38:33Z"},
//         "user_name": "winner_trader",
//         "stock": ["$SPX", "$SPY", "$ES"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c1f"},
//         "text": "$SPX 15 min Engulf red candle $SPY https://t.co/RnmnI3Fh5x",
//         "created_at": {"$date": "2019-11-12T19:16:06Z"},
//         "user_name": "winner_trader",
//         "stock": ["$SPX", "$SPY"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c20"},
//         "text": "$TSLA now 345 . forming bearish candle on daily targeting 328 https://t.co/3xg4aXX6sV",
//         "created_at": {"$date": "2019-11-12T19:13:15Z"},
//         "user_name": "winner_trader",
//         "stock": ["$TSLA"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c21"},
//         "text": "$INTC 1900 Put contracts 20 Dec 52.5 @ 0.22",
//         "created_at": {"$date": "2019-11-12T17:11:45Z"},
//         "user_name": "winner_trader",
//         "stock": ["$INTC"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c22"},
//         "text": "$OSTK Daily .. Risky but oversold!! https://t.co/25TffPWgHS",
//         "created_at": {"$date": "2019-11-11T20:52:14Z"},
//         "user_name": "winner_trader",
//         "stock": ["$OSTK"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c23"},
//         "text": "$BA what A bounce from 345 to 358 !!",
//         "created_at": {"$date": "2019-11-11T16:59:37Z"},
//         "user_name": "winner_trader",
//         "stock": ["$BA"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c24"},
//         "text": "Weakness continuous for $AMZN and $FB compared by strength of $AAPL and $MSFT..",
//         "created_at": {"$date": "2019-11-11T16:58:39Z"},
//         "user_name": "winner_trader",
//         "stock": ["$AMZN", "$FB", "$AAPL", "$MSFT"],
//         "retweet_count": 0
//     },
//     {
//         "_id": {"$oid": "5dcbefee8aad706ad9976c25"},
//         "text": "$LYFT Drop by 3% at 41.8 https://t.co/pSW4KiXWRE",
//         "created_at": {"$date": "2019-11-11T15:53:05Z"},
//         "user_name": "winner_trader",
//         "stock": ["$LYFT"],
//         "retweet_count": 2
//     }
// ])
//
