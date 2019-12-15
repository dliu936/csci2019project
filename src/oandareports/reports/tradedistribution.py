import os
import matplotlib.pylab as plt
import dask.dataframe as dd
import numpy as np
import pandas as pd
from luigi import Task, build
from ..helperfiles.task import TargetOutput
from pandas.plotting import register_matplotlib_converters
from ..tools.historicrates import GetHistoricRates
import datetime as datetime
import plotly.graph_objects as go
import plotly.express as px

register_matplotlib_converters()


class TradeDistributionReport(Task):

    # Set output location
    # output = TargetOutput(os.getenv('local_location') + '/image')
    # Placeholder for plot
    fig = object

    def order_flow(self, dsk):
        df = dsk.compute()
        for i in df["instrument"].unique():
            temp_df = df[df["instrument"] == i]
            temp_df = temp_df.copy()
            temp_df["transaction"] = np.where(temp_df.units > 0, 1, 0)
            task = build(
                [GetHistoricRates(instrument=i, granularity="H1")], local_scheduler=True
            )
            ddf_rate = dd.read_parquet(
                os.getenv("local_location")
                + "rates/"
                + i
                + "_"
                + "H1"
                + "/"
                + "part.*.parquet"
            )
            ddf_rate["time"] = dd.to_datetime(ddf_rate["time"])
            ddf_rate = ddf_rate[["c", "time"]]
            ddf_rate["close"] = ddf_rate["c"].astype("float64")
            ddf_rate = ddf_rate.compute()
            fig, ax = plt.subplots()
            scatter = ax.scatter(temp_df["time"], temp_df["price"], c=temp_df["transaction"])
            ax.plot(ddf_rate["time"], ddf_rate["close"], alpha=0.4)
            plt.xlim(
                temp_df["time"].max() - datetime.timedelta(days=30),
                temp_df["time"].max(),
            )
            plt.xticks(rotation=45)
            plt.ylabel("USD")
            plt.title("Transactions for {}".format(i))
            plt.legend(handles=scatter.legend_elements()[0],labels=['Sell','Buy'])
            fig.savefig(
                os.getenv("local_location") + "images/" + "order_flow_{}.png".format(i)
            )
            # Placeholder for plot
            self.fig.append(plt)



    def run(self):
        def buyUnits(units):
            if (units > 0):
                return units
            else:
                return 0

        def sellUnits(units):
            if (units < 0):
                return abs(units)
            else:
                return 0

        def tradeType(units):
            if (units >= 0):
                return "buy"
            else:
                return "sell"


        dsk = dd.read_parquet(os.getenv("local_location") + "trading_history/*.parquet", columns=["time", "type", "instrument", "units"])
        dsk["time"] = dsk["time"].astype("M8[D]")
        dsk['type'] = dsk['type'].astype('str')
        dsk['instrument'] = dsk['instrument'].astype('str')
        dsk["day"] = dsk["time"].dt.day_name()
        # get only rows with ORDER_FILL
        dsk = dsk[(dsk['type'] == 'ORDER_FILL')]
        dsk['units'] = dsk['units'].astype('int')
        # Find the buy and sell rows
        # dsk = dsk.assign(buy_units=dsk['units'] if dsk['units'] >= 0 else 0,
        #                  sell_units=abs(dsk['units']) if dsk['units'] >= 0 else 0)
        dsk['buy_units'] = dsk.apply(lambda x: buyUnits(x['units']), axis=1)
        dsk['sell_units'] = dsk.apply(lambda x: sellUnits(x['units']), axis=1)
        dsk['action'] = dsk.apply(lambda x: tradeType(x['units']), axis=1)
        #dsk['sell_units'] = abs(dsk['units']) if dsk['units'] < 0 else 0
        dsk.set_index('day')

        print(dsk.head(10))
        #dsk = dsk.groupby(['day']).count()
        #print(dsk.head(10))
        #df["date"] = pd.to_datetime(dsk["time"])

        dsk = dsk[["day", "type", "instrument", "units", "buy_units", "sell_units", "action"]]

        self.trade_distribution(dsk)


    def trade_distribution(self, dsk):

        # fig = px.bar(dsk, x="day", y="units", color="action", barmode="group", facet_row="instrument", facet_col="day",
        #              category_orders={0: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        #                               2: ["AUD_CHF","AUD_SGD"]})
                                                     # "BCO_USD",
                                                     # "EUR_CAD",
                                                     # "EUR_USD",
                                                     # "USD_SEK",
                                                     # "USD_NOK",
                                                     # "USD_THB",
                                                     # "XCU_USD"
                                                     #]})

        #df = dsk.compute()
        #print(df.head(5))
        df = dsk.compute().values
        print(df[0:10])
        fig = px.bar(df, x=0, y=3, color=6, barmode="group", facet_row=2, facet_col=0,
                     category_orders={0: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                      2: ["AUD_CHF",
                                                     "AUD_SGD",
                                                     # "BCO_USD",
                                                     # "EUR_CAD",
                                                     # "EUR_USD",
                                                     # "USD_SEK",
                                                     # "USD_NOK",
                                                     # "USD_THB",
                                                     # "XCU_USD"
                                                     ]})

        # fig = px.bar(df, x="day", y="units", color="type", barmode="group", facet_row="instrument", facet_col="day",
        #              category_orders={"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        #                               "instrument": ["AUD_CHF",
        #                                              "AUD_SGD",
        #                                              "BCO_USD",
        #                                              "EUR_CAD",
        #                                              "EUR_USD",
        #                                              "USD_SEK",
        #                                              "USD_NOK",
        #                                              "USD_THB",
        #                                              "XCU_USD"
        #                                              ]})
        #fig.write_image(file=os.getenv("local_location") + "images/" + "trade_distribution.png", format='png')
        #fig.show()
        self.fig = fig


        # fig = go.Figure(data=[go.Candlestick(x=df['Date'],
        #                                      open=df['AAPL.Open'], high=df['AAPL.High'],
        #                                      low=df['AAPL.Low'], close=df['AAPL.Close'])
        #                       ])

        # fig.update_layout(
        #     title='Trade Distribution',
        #     yaxis_title='USD/EUR',
        #     shapes=[dict(
        #         x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        #         line_width=2)],
        #     annotations=[dict(
        #         x='2016-12-09', y=0.05, xref='x', yref='paper',
        #         showarrow=False, xanchor='left', text='Increase Period Begins')]
        # )
        # div = opy.plot(fig, auto_open=False, output_type='div')

