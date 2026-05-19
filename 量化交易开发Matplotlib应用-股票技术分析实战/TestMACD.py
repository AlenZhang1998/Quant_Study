import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体（macOS 使用 PingFang SC 或 Arial Unicode MS）
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

from unittest import TestCase

class TestMACD(TestCase):
    """
    MACD（Moving Average Convergence Divergence）指标计算类
    MACD由三部分组成：
    - DIF线：快速EMA与慢速EMA的差值
    - DEA线：DIF的EMA（信号线）
    - MACD柱：DIF与DEA差值的2倍
    """

    def cal_macd(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        计算MACD指标

        参数:
            df: 包含股票数据的DataFrame
            fastperiod: 快速EMA周期，默认12
            slowperiod: 慢速EMA周期，默认26
            signalperiod: 信号线周期，默认9

        返回:
            添加了DIF、DEA、MACD柱的DataFrame
        """
        # 计算12日EMA（快速移动平均线）
        ewma12 = df['close'].ewm(span=fastperiod, adjust=False).mean()
        # 计算26日EMA（慢速移动平均线）
        ewma26 = df['close'].ewm(span=slowperiod, adjust=False).mean()

        # DIF = 快速EMA - 慢速EMA
        df['dif'] = ewma12 - ewma26
        # DEA = DIF的9日EMA（信号线）
        df['dea'] = df['dif'].ewm(span=signalperiod, adjust=False).mean()
        # MACD柱 = (DIF - DEA) * 2
        df['bar'] = (df['dif'] - df['dea']) * 2

        return df

    def test_MACD(self):
        """测试MACD计算并绘制图表"""
        # 读取股票数据CSV文件
        file_name = "/Users/alan2/Downloads/quant/数据/demo.csv"
        df = pd.read_csv(file_name)

        # 设置列名：股票代码、日期、收盘价、开盘价、最高价、最低价、成交量
        df.columns = ["stock_id", "date", "close", "open", "high", "low", "volume"]
        # 选择需要的列
        df = df[["date", "close", "open", "high", "low", "volume"]]
        # 将日期列转换为datetime类型
        df["date"] = pd.to_datetime(df["date"])

        # 计算MACD指标
        df_macd = self.cal_macd(df)
        print(df_macd)

        # 创建图表
        plt.figure()

        # 绘制DEA线（红色）和DIF线（蓝色）
        df_macd['dea'].plot(color="red", label='dea')
        df_macd['dif'].plot(color="blue", label='dif')
        plt.legend(loc='best')

        # 分离正负MACD柱
        pos_bar = []    # 正值柱状图数据
        pos_index = []  # 正值柱状图索引
        neg_bar = []    # 负值柱状图数据
        neg_index = []  # 负值柱状图索引

        # 遍历数据，分离正负值
        for index, row in df_macd.iterrows():
            if(row['bar'] > 0):
                pos_bar.append(row['bar'])
                pos_index.append(index)
            else:
                neg_bar.append(row['bar'])
                neg_index.append(index)

        # 绘制MACD柱状图
        # 大于0用红色表示（多头力量）
        plt.bar(pos_index, pos_bar, width=0.5, color='red')
        # 小于等于0则用绿色表示（空头力量）
        plt.bar(neg_index, neg_bar, width=0.5, color='green')

        # 设置X轴刻度标签为日期
        major_index = df_macd.index[df_macd.index] # major_index = df_macd.index
        major_xtics = df_macd['date'][df_macd.index] # major_xtics = df_macd['date']
        plt.xticks(major_index, major_xtics)
        # 旋转X轴标签30度，避免重叠
        plt.setp(plt.gca().get_xticklabels(), rotation=30)

        # 设置图表样式
        plt.grid(linestyle='-.')  # 网格线
        plt.title('000001平安银行MACD图')
        plt.show()





# ⏺ ewm 是 pandas 中的 指数加权移动平均（Exponentially Weighted Moving Average）方法。

#   核心特点：
#   - 越近的数据权重越大，越远的数据权重越小
#   - 权重按指数衰减

#   代码中的用法：
#   ewma12 = df['close'].ewm(span=12, adjust=False).mean()

#   参数说明：
#   - span=12 - 周期为12，衰减因子 α = 2/(span+1) = 2/13 ≈ 0.154
#   - adjust=False - 使用递归计算方式，更符合技术分析标准

#   与普通MA的区别：

#   ┌────────────────────┬─────────────────────────┐
#   │ MA（简单移动平均） │ EMA（指数加权移动平均） │
#   ├────────────────────┼─────────────────────────┤
#   │ 所有权重相同       │ 近期权重更大            │
#   ├────────────────────┼─────────────────────────┤
#   │ 反应较慢           │ 反应更灵敏              │
#   ├────────────────────┼─────────────────────────┤
#   │ 对新数据不敏感     │ 对新数据更敏感          │
#   └────────────────────┴─────────────────────────┘

#   在MACD指标中，EMA能更快反映价格变化，所以用它来计算DIF线。