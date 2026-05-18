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
    # def testKLineChart(self):
    #     file_name = "../数据/demo.csv"
    #     df = pd.read_csv(file_name, header=None)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]
    #     df["date"] = pd.to_datetime(df["date"]) # 把字符串变时间。
    #     df = df.set_index("date") # 把 date 这一列变成“索引”
    #     df = df[["close","open","high","low","volume"]]
    #     print("数据预览:")
    #     print(df.head()) # 只看前5行
    #     # print(df) # 打印整个 DataFrame

    #     # 设置K线颜色 ohlc='i'开高低收颜色跟随K线； wick='i'上下影线跟随K线颜色
    #     my_color = mpf.make_marketcolors(
    #         up='red', down='green',
    #         wick='i', volume={'up':'red','down':'green'}, ohlc='i'
    #     )

    #     # 设置整体风格 定义K线图整体主题
    #     my_style = mpf.make_mpf_style(
    #         marketcolors=my_color, gridaxis='both', gridstyle='-.' # gridaxis='both' 横纵网格都显示; gridstyle='-.' 点划线风格
    #     )
    #     # 真正画图
    #     # type='candle 画蜡烛图（K线）
    #     # savefig='kline.png' 把图保存成图片
    #     mpf.plot(df, type='candle', title='K-Line', ylabel='price',
    #              style=my_style, volume=True, ylabel_lower='volume',
    #              datetime_format='%Y-%m-%d', xrotation=45,
    #              savefig='kline.png')
    #     print("\nK线图已保存为 kline.png")



    # #K线图带交易量
    # def testKLineByVolume(self):
    #     file_name = "../数据/demo.csv"
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
    #         df,                             # 要画的数据，必须是 DataFrame，且索引为日期
    #         type = 'candle',                # 图表类型：蜡烛图（K线）
    #         title = 'K-LineByVolume',       # 图表标题
    #         ylabel = 'price',               # 左侧Y轴标签（价格）
    #         style = my_style,               # 应用之前定义的K线样式
    #         show_nontrading = False,        # 不显示非交易日（如周末、节假日）
    #         volume = True,                  # 显示成交量子图
    #         ylabel_lower = 'volume',        # 下方成交量子图的Y轴标签
    #         datetime_format = '%Y-%m-%d',   # X轴日期格式：年-月-日
    #         xrotation = 45,                 # X轴日期标签旋转45度，防止重叠
    #         linecolor = '#00ff00',          # 收盘价连线颜色（绿色），用于非蜡烛图类型
    #         tight_layout = False,           # 不使用紧凑布局，保留默认边距
    #         savefig='kline.png'             # 将图表保存为 kline.png 文件
    #     )




    # K线图带交易量及均线
    def testKLineByMA(self):
        file_name = "../数据/demo.csv"
        df = pd.read_csv(file_name)
        df.columns = ["stock_id","date","close","open","high","low","volume"]
        df = df[["date","close","open","high","low","volume"]]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index('date')

        my_color = mpf.make_marketcolors(
            up = 'red',
            down = 'green',
            wick = 'i',
            volume = {'up':'red','down':'green'},
            ohlc = 'i'
        )

        my_style  = mpf.make_mpf_style(
            marketcolors = my_color,        # 应用之前定义的K线涨跌颜色方案
            gridaxis = 'both',              # 横纵网格线都显示
            gridstyle = '-.',               # 网格线样式：点划线
            rc = {'font.family':'STSong'}   # 设置字体为宋体，确保中文正常显示
        )

        mpf.plot(
            df,                             # 要画的数据，必须是 DataFrame，且索引为日期
            type = 'candle',                # 图表类型：蜡烛图（K线）
            mav = [5,10, 15],                   # 叠加5日和10日移动平均线（MA5、MA10）
            title='K-LineByVolume',         # 图表标题
            ylabel='price',                 # 左侧Y轴标签（价格）
            style=my_style,                 # 应用之前定义的K线样式
            show_nontrading=False,          # 不显示非交易日（如周末、节假日）
            volume=True,                    # 显示成交量子图
            ylabel_lower='volume',          # 下方成交量子图的Y轴标签
            datetime_format='%Y-%m-%d',     # X轴日期格式：年-月-日
            xrotation=45,                   # X轴日期标签旋转45度，防止重叠
            linecolor='#00ff00',            # 收盘价连线颜色（绿色），用于非蜡烛图类型
            tight_layout=False,             # 不使用紧凑布局，保留默认边距
            savefig='kline.png'             # 将图表保存为 kline.png 文件
        )
