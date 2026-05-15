import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from unittest import TestCase

# import pandas as pd

# df = pd.read_csv('btc.csv')

# df['date'] = pd.to_datetime(df['date'])

# df = df.set_index('date')

# df['ma5'] = df['close'].rolling(5).mean()

# df['return'] = df['close'].pct_change()

class TestPandasKline(TestCase):
    #读取股票数据，画出K线图
    def testKLineChart(self):
        file_name = "../数据/demo.csv"
        df = pd.read_csv(file_name, header=None)
        df.columns = ["stock_id","date","close","open","high","low","volume"]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        df = df[["close","open","high","low","volume"]]
        print("数据预览:")
        print(df.head())

        my_color = mpf.make_marketcolors(
            up='red', down='green',
            wick='i', volume={'up':'red','down':'green'}, ohlc='i'
        )
        my_style = mpf.make_mpf_style(
            marketcolors=my_color, gridaxis='both', gridstyle='-.'
        )
        mpf.plot(df, type='candle', title='K-Line', ylabel='price',
                 style=my_style, volume=True, ylabel_lower='volume',
                 datetime_format='%Y-%m-%d', xrotation=45,
                 savefig='kline.png')
        print("\nK线图已保存为 kline.png")



    # #K线图带交易量
    # def testKLineByVolume(self):
    #     file_name = "./demo.csv"
    #     df = pd.read_csv(file_name)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]
    #     df = df[["date","close","open","high","low","volume"]]
    #     df["date"] = pd.to_datetime(df["date"]) # 把字符串转时间
    #     df = df.set_index('date')

    #     my_color = mpf.make_marketcolors(
    #         up = 'red',
    #         down = 'green',
    #         wick = 'i',
    #         volume = {'up':'red','down':'green'},
    #         ohlc = 'i'
    #     )

    #     my_style  = mpf.make_mpf_style(
    #         marketcolors = my_color,
    #         gridaxis = 'both',
    #         gridstyle = '-.',
    #         rc = {'font.family':'STSong'}
    #     )

    #     mpf.plot(
    #         df,
    #         type = 'candle',
    #         title = 'K-LineByVolume',
    #         ylabel = 'price',
    #         style = my_style,
    #         show_nontrading = False,
    #         volume = True,
    #         ylabel_lower = 'volume',
    #         datetime_format = '%Y-%m-%d',
    #         xrotation = 45,
    #         linecolor = '#00ff00',
    #         tight_layout = False
    #     )




    # # K线图带交易量及均线
    # def testKLineByMA(self):
    #     file_name = "./demo.csv"
    #     df = pd.read_csv(file_name)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]
    #     df = df[["date","close","open","high","low","volume"]]
    #     df["date"] = pd.to_datetime(df["date"])
    #     df = df.set_index('date')

    #     my_color = mpf.make_marketcolors(
    #         up = 'red',
    #         down = 'green',
    #         wick = 'i',
    #         volume = {'up':'red','down':'green'},
    #         ohlc = 'i'
    #     )

    #     my_style  = mpf.make_mpf_style(
    #         marketcolors = my_color,
    #         gridaxis = 'both',
    #         gridstyle = '-.',
    #         rc = {'font.family':'STSong'}
    #     )

    #     mpf.plot(
    #         df,
    #         type = 'candle',
    #         mav = [5,10],
    #         title='K-LineByVolume',
    #         ylabel='price',
    #         style=my_style,
    #         show_nontrading=False,
    #         volume=True,
    #         ylabel_lower='volume',
    #         datetime_format='%Y-%m-%d',
    #         xrotation=45,
    #         linecolor='#00ff00',
    #         tight_layout=False
    #     )
