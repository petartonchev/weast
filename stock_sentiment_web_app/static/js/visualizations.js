function visualizeCharts(sentiment, sentiment_trend, stock_ticker) {

    let sentiment_lookup = convertSentimentToDict(sentiment_trend);

        // Sentiment Chart
        Highcharts.chart('sentiment-chart', {
            chart: {
                marginTop: 40,
                inverted: true,
                marginLeft: 8,
                type: 'bullet',
                backgroundColor: 'transparent'
            },
            title: {
                text: 'Overall Sentiment'
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    pointPadding: 0.35,
                    borderWidth: 0,
                    color: '#252525',
                    targetOptions: {
                        width: '200%'
                    }
                }
            },
            credits: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            xAxis: {
                categories: [null]
            },
            yAxis: {
                min: -1,
                max: 1,
                endOnTick: false,
                gridLineWidth: 0,
                plotBands: [{
                    from: -1,
                    to: -0.15,
                    color: '#f60239'
                }, {
                    from: -0.15,
                    to: 0.15,
                    color: '#999'
                }, {
                    from: 0.15,
                    to: 1,
                    color: '#4c9d49'
                }],
                title: null
            },
            series: [{
                data: [{
                    y: sentiment,
                    target: sentiment
                }]
            }],
            tooltip: {
                pointFormat: '<b>Sentiment: {point.y}</b>',
                valueDecimals: 2
            }
        });

    fetchPriceData(stock_ticker).then(function (price_data) {

        let perc_change = calcPercChange(sentiment_lookup, price_data);

        // Trend Chart
        Highcharts.chart('trend-chart', {
            chart: {
                zoomType: 'x',
                backgroundColor: 'transparent'
            },
            title: {
                text: 'Real Stock Price vs Sentiment over Time'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}$',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                title: {
                    text: 'Adj Close',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }
            }, { // Secondary yAxis
                max: 1,
                min: -1,
                endOnTick: false,
                title: {
                    text: 'Sentiment',
                    style: {
                        color: '#4c9d49'
                    }
                },
                labels: {
                    style: {
                        color: '#4c9d49'
                    }
                },
                opposite: true
            }],
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                },
                column: {

                    opacity: 0.7,
                    zones: [{
                        value: 0,
                        color: '#f60239'
                    }, {
                        color: '#4c9d49'
                    }]
                }
            },

            series: [{
                type: 'area',
                name: 'Adj Close',
                data: price_data
            }, {
                type: 'column',
                name: 'Twitter Sentiment',
                yAxis: 1,
                data: sentiment_trend
            }]
        });

        // Percentage Change Chart
        Highcharts.chart('perc-change-chart', {
            chart: {
                zoomType: 'x',
                backgroundColor: 'transparent'
            },
            colorAxis: {
                min: -1,
                max: 1,
                dataClasses: [{
                    from: -1,
                    to: 0,
                    color: '#f60239'
                }, {
                    from: 0,
                    to: 1,
                    color: '#4c9d49'
                }]
            },
            title: {
                text: 'Percentage Change in Stock Price vs Sentiment over Time'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}%',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                title: {
                    text: 'Percentage Change',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }
            }],
            legend: {
                enabled: false
            },
            plotOptions: {
                column: {
                    opacity: 0.7
                }
            },

            series: [{
                type: 'column',
                name: 'Percentage Change',
                data: perc_change,
                colorKey: 'sentiment',
                color: 'grey',
            }],
            tooltip: {
                pointFormat: '<b>Sentiment: {point.sentiment}</b><br><b>Percentage Change: {point.y}%</b>',
                valueDecimals: 2
            }
        });

    });
}


async function fetchPriceData(stock_ticker) {
    let stocks = new Stocks('N6VYEDBTYS8L175P');

    let today = new Date();
    const data = await stocks.timeSeries({
        symbol: stock_ticker,
        interval: 'daily',
        start: new Date(today.setMonth(today.getMonth() - 1)),
        end: new Date()
    });

    data.sort((a, b) => (a.date > b.date) ? 1 : -1);
    return data.map(function (day) {
        return [day.date.getTime(), day.close]
    })
}

function convertSentimentToDict(sentiment_trend) {

    let sentiment_lookup = {};

    for (let i = 0; i < sentiment_trend.length; i++) {
        let date, sentiment;
        [date, sentiment] = sentiment_trend[i];
        date = new Date(date);
        // Set hours to the close time of the stock market
        date.setHours(6, 0, 0, 0);
        // Convert back to timestamp
        date = date.getTime();
        sentiment_lookup[date] = sentiment;
    }


    return sentiment_lookup;
}

function calcPercChange(sentiment_lookup, price_data) {
    let perc_change = [];
    for (let i = 1; i < price_data.length; i++) {
        let curr_date, curr_price;
        [curr_date, curr_price] = price_data[i];

        let price_yesterday = price_data[i - 1][1];
        let curr_perc_change = (curr_price - price_yesterday) / price_yesterday * 100
        perc_change.push({
            x: curr_date,
            y: curr_perc_change,
            sentiment: sentiment_lookup[curr_date]
        })
    }
    return perc_change;

}
