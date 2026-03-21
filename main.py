# 引入TqSdk模块
from tqsdk import TqApi, TqAuth
import pandas as pd

# 创建api实例，设置web_gui=True生成图形化界面
api = TqApi(auth=TqAuth("walkercook", "b#K6x*T3vM@cTq"))
# 订阅 au2506 合约的10秒线
klines = api.get_kline_serial(symbol="DCE.i2605", duration_seconds=900, data_length=512)

# 生成示例 K 线数据
data = pd.DataFrame({
    "Date": pd.to_datetime(klines["datetime"]),
    "Open": klines["open"],
    "High": klines["high"],
    "Low": klines["low"],
    "Close": klines["close"],
    "Volume": klines["volume"],
})


# 只保留需要的四列
df = klines[['high', 'low']].copy()

# 加 Line 列，从 1 开始编号
df['line'] = range(1, len(df) + 1)

# 直接存成 csv，带标题，默认用逗号分隔
df.to_csv("kline_ohlc.csv", index=False, encoding="utf-8")
# 如果你想确认一下文件内容，可以先打印前几行看
print(df.head())

# 关闭api,释放资源
api.close()

#klines.to_json("kline_data.json", orient="records", lines=True,date_format="iso", force_ascii=False)
