import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from unittest import TestCase

file_name = "../数据/demo.csv"

# import pandas as pd

# df = pd.read_csv('btc.csv')

# df['date'] = pd.to_datetime(df['date'])

# df = df.set_index('date')

# df['ma5'] = df['close'].rolling(5).mean()

# df['return'] = df['close'].pct_change()

class TestPandasStock(TestCase):
    #读取文件
    # def testReadFile(self):
    #     df = pd.read_csv(file_name, header=None)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]

    #     print(27, df.info())
    #     print("-------------")
    #     print(29, df.describe())


    #时间处理
    def testTime(self):
        df = pd.read_csv(file_name, header=None)
        df.columns = ["stock_id","date","close","open","high","low","volume"] # 设置列名

        df["date"] = pd.to_datetime(df["date"]) # 把字符串转时间为： Timestamp('2009-01-05')

        # 加上year month列
        df["year"] = df["date"].dt.year 
        df["month"] = df["date"].dt.month

        print('时间处理',df)





    # # 最低收盘价
    # def testCloseMin(self):
    #     df = pd.read_csv(file_name, header=None)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]

    #     print("""close min : {}""".format(df["close"].min())) # 找 close 列最小值
    #     print("""close min index : {}""".format(df["close"].idxmin())) # 找“最小值所在的行索引” 它在哪一行
    #     print("""close min frame : {}""".format(df.loc[df["close"].idxmin()])) # 取close最小值那行的完整数据




    # # 每月平均收盘价与开盘价
    # def testMean(self):
    #     df = pd.read_csv(file_name, header=None)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]

    #     df["date"] = pd.to_datetime(df["date"])
    #     df["month"] = df["date"].dt.month

    #     print("""month close mean : {}""".format(df.groupby("month")["close"].mean())) # 按“月份”分组，然后计算每个月的平均收盘价
    #     print("""month open mean : {}""".format(df.groupby("month")["open"].mean()))



    # 计算涨跌幅
    # 涨跌幅今日收盘价减去昨日收盘价
    # def testRipples_ratio(self):
    #     df = pd.read_csv(file_name, header=None)
    #     df.columns = ["stock_id","date","close","open","high","low","volume"]

    #     df["date"] = pd.to_datetime(df["date"])

    #     df["rise"] = df["close"].diff() # （今天收盘价 - 昨天收盘价）  /   上一天的收盘价
    #     df["rise_ratio"] = df["rise"] / df.shift(1)["close"]   # +1 = 数据往下走（视觉下移）
    #     # df["rise_ratio"] = df['close'].pct_change() * 100 # 最推荐写法（工业标准）


    #     print('涨跌幅',df)

    # 计算股价移动平均
    def testMA(self):
        df = pd.read_csv(file_name, header=None)
        df.columns = ["stock_id","date","close","open","high","low","volume"]

        df['ma_5'] = df.close.rolling(window=5).mean() # MD5
        df['ma_10'] = df.close.rolling(window=10).mean() # MD10
        df = df.fillna(0)

        print('平均收盘价',df)


