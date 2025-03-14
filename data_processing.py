import pandas as pd
import json

# TODO: 这里可以写一个将excel文件转换为json或csv文件的模块调用
ds = pd.read_csv("log.csv")
ds["时间"] = pd.to_datetime(
    ds["时间"], format="%m-%d %H:%M:%S", errors="coerce").dt.date
ds['访问次数'] = 1
result = ds.groupby(["时间", "模型"])["访问次数"].sum().reset_index()
l_result = result.pivot(index="时间", columns="模型", values="访问次数").fillna(0)
# 直接保存为CSV
l_result.to_csv("apiperday.csv")

# 读取处理后的CSV文件
df = pd.read_csv("apiperday.csv")
df = df.astype(str)
# 转换为ECharts所需的JSON格式
data_json = df.to_dict(orient="records")

# 保存为JSON文件
with open("apiperday.json", "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)
