import pandas as pd
import matplotlib.pyplot as plt


from unittest import TestCase

class TestKDJ(TestCase):
    def cal_kdj(self,df):
        # ========== 计算 KDJ 指标 ==========
        # RSV (Raw Stochastic Value) = (收盘价 - 最低价) / (最高价 - 最低价) * 100
        # RSV 反映当前收盘价在过去9日价格区间中的相对位置

        # 计算9日滚动最低价，不足9日时用扩展窗口的最小值填充
        low_list = df['low'].rolling(9,min_periods=9).min() # min_periods至少要9天的数据
        # 填充空值 给 NaN 找替代值
        low_list.fillna(value=df['low'].expanding().min(),inplace=True) # 前面数据不足时：用目前为止最低价
        # 计算9日滚动最高价，不足9日时用扩展窗口的最大值填充
        high_list = df['high'].rolling(9,min_periods=9).max()
        high_list.fillna(value=df['high'].expanding().max(),inplace=True)
        # 计算 RSV：收盘价在9日高低区间中的百分比位置
        rsv = (df['close'] - low_list) / (high_list - low_list) * 100
        # K 值：对 RSV 做指数加权移动平均（com=2 即 span=5）
        df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
        # D 值：对 K 值再做一次指数加权移动平均
        df['d'] = df['k'].ewm(com=2).mean()
        # J 值：3K - 2D，放大 K 与 D 的偏离程度，是最敏感的信号线
        df['j'] = 3 * df['k'] - 2 * df['d']
        return df

    def test_KDJ(self):
        # ========== 读取股票数据 ==========
        file_name = "/Users/alan2/Downloads/quant/数据/demo.csv"
        df = pd.read_csv(file_name)
        # 设置列名：股票代码、日期、收盘价、开盘价、最高价、最低价、成交量
        df.columns = ["stock_id","date","close","open","high","low","volume"]
        # 只保留需要的列，去掉股票代码
        df = df[["date","close","open","high","low","volume"]]
        # 将日期列转为 datetime 类型
        df["date"] = pd.to_datetime(df["date"])

        # ========== 计算 KDJ 并打印结果 ==========
        df_kdj = self.cal_kdj(df)
        print(df_kdj)

        # ========== 绘制 KDJ 图表 ==========
        plt.figure()
        # 绘制 K 线（红色）、D 线（黄色）、J 线（蓝色）
        df_kdj['k'].plot(color="red",label='k')
        df_kdj['d'].plot(color="yellow",label='d')
        df_kdj['j'].plot(color="blue",label='j')
        # 显示图例，自动选择最佳位置
        plt.legend(loc='best')

        # 设置 X 轴刻度标签为日期，旋转30度避免重叠
        major_index = df_kdj.index[df_kdj.index]
        major_xtics = df_kdj['date'][df_kdj.index] # df_kdj['date']
        plt.xticks(major_index,major_xtics)
        plt.setp(plt.gca().get_xticklabels(),rotation=30)

        # 添加网格线、标题，设置中文字体
        plt.grid(linestyle='-.')
        plt.title('000001平安银行KDJ图')
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.show()

    def testBoll(self):
        # ========== 布林带 (Bollinger Bands) 计算与绘制 ==========
        # 布林带由三条线组成：中轨(SMA)、上轨(SMA+2σ)、下轨(SMA-2σ)
        # 用于衡量价格的波动范围和超买超卖状态
        import numpy as np
        from matplotlib.pyplot import plot
        from matplotlib.pyplot import show

        N = 5  # 移动平均窗口大小

        # 均等权重，用于计算简单移动平均 (SMA)
        weights = np.ones(N) / N
        print("Weights", weights)

        # 从 CSV 第3列（索引2，即收盘价）加载数据
        c = np.loadtxt('demo.csv', delimiter=',', usecols=(2,), unpack=True)
        # 用卷积计算 SMA，截取有效部分
        sma = np.convolve(weights, c)[N - 1:-N + 1]
        deviation = []
        C = len(c)

        # 计算每个窗口的标准差（用于上下轨）
        for i in range(N - 1, C):
            if i + N < C:
                dev = c[i: i + N]
            else:
                dev = c[-N:]

            # 计算当前窗口数据与 SMA 的偏差
            averages = np.zeros(N)
            averages.fill(sma[i - N - 1])
            dev = dev - averages
            dev = dev ** 2
            dev = np.sqrt(np.mean(dev))  # 标准差
            deviation.append(dev)

        # 上下轨偏离量 = 2倍标准差
        deviation = 2 * np.array(deviation)
        print(len(deviation), len(sma))
        # 上轨 = SMA + 2σ，下轨 = SMA - 2σ
        upperBB = sma + deviation
        lowerBB = sma - deviation

        # 计算收盘价落在布林带内的比例
        c_slice = c[N - 1:]
        between_bands = np.where((c_slice < upperBB) & (c_slice > lowerBB))

        print(lowerBB[between_bands])
        print(c[between_bands])
        print(upperBB[between_bands])
        between_bands = len(np.ravel(between_bands))
        print("Ratio between bands", float(between_bands) / len(c_slice))

        # 绘制布林带：收盘价、SMA、上轨、下轨
        t = np.arange(N - 1, C)
        plot(t, c_slice, lw=1.0)   # 收盘价曲线（细线）
        plot(t, sma, lw=2.0)        # 中轨 SMA
        plot(t, upperBB, lw=3.0)    # 上轨
        plot(t, lowerBB, lw=4.0)    # 下轨
        show()