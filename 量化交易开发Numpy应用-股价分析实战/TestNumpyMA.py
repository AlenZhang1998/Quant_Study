import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from unittest import TestCase

file_name = "/Users/alan2/Downloads/quant/数据/demo.csv"

class TestNumpyMA(TestCase):

    def testSMA(self):
        # 读取股票收盘价
        end_price = np.loadtxt(
            fname=file_name,
            delimiter=',',
            usecols=(3),
            unpack=True
        )
        print("收盘价:", end_price)
        N = 5 # 5日均线
        weights = np.ones(N) / N # 每一天权重一样
        print("权重:", weights)
        sma = np.convolve(weights, end_price)[N-1:-N+1] # 卷积   [N-1:-N+1]：切掉边缘垃圾数据
        print("SMA:", sma) # 五日均线
        plt.figure(figsize=(12, 6))
        plt.plot(sma, linewidth=2, label='SMA(5)')
        plt.plot(end_price[N-1:], linewidth=1, alpha=0.5, label='收盘价')
        plt.legend()
        plt.title('简单移动平均线 SMA')
        plt.savefig('sma.png')
        print("SMA图表已保存为 sma.png")

    # def testEXP(self):
    #     x = np.arange(5)
    #     y = np.arange(10)
    #     print("x", x)
    #     print("y", y)
    #     print("""Exp x : {}""".format(np.exp(x))) # 指数函数 e的x次方
    #     print("""Exp y : {}""".format(np.exp(y))) # 指数函数 e的y次方
    #     print("""Linespace : {}""".format(np.linspace(-1, 0, 5)))

    #     # np.linspace(-1, 0, 5) 在线段中平均取点 得到 [-1.   -0.75  -0.5  -0.25  0.]

    # 指数移动曲线
    def testEMA(self):
        end_price = np.loadtxt(
            fname=file_name,
            delimiter=',',
            usecols=(3),
            unpack=True
        )
        print("收盘价:", end_price)
        N = 5
        weighs = np.exp(np.linspace(-1, 0, N)) # 越靠近现在：权重越大。
        weighs /= weighs.sum() # 权重总和必须=1
        print("EMA权重:", weighs)
        ema = np.convolve(weighs, end_price)[N-1:-N+1]
        print("EMA:", ema)

        t = np.arange(N-1, len(end_price))
        plt.figure(figsize=(12, 6))
        plt.plot(t, end_price[N-1:], lw=1.0, alpha=0.5, label='收盘价')
        plt.plot(t, ema, lw=2.0, label='EMA(5)')
        plt.legend()
        plt.title('指数移动平均线 EMA')
        plt.savefig('ema.png')
        print("EMA图表已保存为 ema.png")





# SMA 和 EMA 的本质区别： 权重不同

# 🎯 SMA（简单移动平均）：权重完全一样
# 🚀 EMA（指数移动平均）：越靠近现在，权重越大
