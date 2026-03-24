from tqsdk import TqApi, TqAccount, TqAuth, TqKq
import pandas as pd

TqAccount()

# 创建api实例，设置web_gui=True生成图形化界面
api = TqApi(auth=TqAuth("walkercook", "b#K6x*T3vM@cTq"))
# 订阅 au2506 合约的10秒线
#klines = api.get_kline_serial(symbol="DCE.i2605", duration_seconds=900, data_length=256)
klines = api.get_kline_serial(symbol="SHFE.au2604", duration_seconds=900, data_length=1024)

# 只保留需要的四列
df = klines[["open", 'high', 'low', "close"]].copy()

# 转置：现在行变成列（每根K线变成一列）
#df_transposed = df.T

# 转成字符串（保留小数位数可自己调）
# 用 .to_string() 比较干净，index 和 columns 都会显示
#text_content = df_transposed.to_string(
#    float_format="{:.1f},".format,  # 保留两位小数，可改成 .4f 等
#    justify="right"                # 右对齐，看起来更整齐
#)
# 极简版：只保留数值，用空格或逗号分隔
#text_content = df_transposed.to_csv(sep=",", header=False, index=False, float_format="%.1f")
text_content = df.to_csv(sep=",", header=False, index=False, float_format="%.2f")

# 先打印到终端
#print("转置后的 OHLC 数据：")
#print(text_content)
#print("\n" + "-"*80 + "\n")  # 分隔线

# 存到 txt 文件
with open("kline.txt", "w", encoding="utf-8") as f:
    f.write(text_content + "\n")



# 加 Line 列，从 1 开始编号
#df['line'] = range(1, len(df) + 1)

# 直接存成 csv，带标题，默认用逗号分隔
#df.to_csv("kline_ohlc.csv", index=False, encoding="utf-8")
# 如果你想确认一下文件内容，可以先打印前几行看
#print(df.head())

# 关闭api,释放资源
api.close()

#klines.to_json("kline_data.json", orient="records", lines=True,date_format="iso", force_ascii=False)
