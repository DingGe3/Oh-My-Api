import pandas as pd
import json
from excel_to_csv import excel_to_csv
import os
from datetime import datetime

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 修改 Python 运行的工作目录
os.chdir(script_dir)

print("当前工作目录:", os.getcwd())  # 确保目录正确

# TODO: 这里可以写一个将excel文件转换为json或csv文件的模块调用
excel_to_csv("data.xlsx","data.csv")


target_date = "03-01"  # 目标截止日期（月-日格式）
default_year = "2025"  # 设定默认年份
date_format = "%Y-%m-%d"  # 日期格式

# 目标日期转换为 datetime（带默认年份）
target_date_dt = pd.to_datetime(f"{default_year}-{target_date}", format=date_format)

# 读取 CSV，按块处理数据
reader = pd.read_csv("data.csv", encoding="utf-8-sig", iterator=True, chunksize=1000)
data_list = []
data_list_others = []
for chunk in reader:
    # 去掉时间部分，仅保留 MM-DD
    chunk["日期"] = chunk["时间"].str[:5]

    # 补充默认年份并转换为 datetime
    chunk["日期"] = pd.to_datetime(f"{default_year}-" + chunk["日期"], format=date_format, errors="coerce")



    # 仅保留目标日期之前的数据
    chunk_filtered = chunk[(chunk["日期"].dt.month == 3) & (chunk["日期"] >= target_date_dt)]
    chunk_others = chunk[chunk["日期"].dt.month != 3]


    # 添加到列表
    data_list.append(chunk_filtered)
    data_list_others.append(chunk_others)

# 合并数据块
ds = pd.concat(data_list, ignore_index=True)
ds_others = pd.concat(data_list_others, ignore_index=True)
print(f"数据处理完成，共合并 {len(ds)} 行")
print(f"其他月份数据处理完成，共合并 {len(ds_others)} 行")
ds['访问次数'] = 1 #：设立新的统计数据访问次数
ds_others['访问次数']=1
ds['时间'] = pd.to_datetime(ds['时间'].str.split(' ').str[0], format='%m-%d', errors='coerce')
ds['时间'] = ds['时间'].dt.strftime('%m-%d')
current_year = str(datetime.now().year)
ds_others['时间'] = pd.to_datetime(
    current_year + '-' + ds_others['时间'].astype(str).str.strip(), 
    format='%Y-%m-%d %H:%M:%S', 
    errors='coerce'
)


ds_others = ds_others.dropna(subset=["时间"])  # 删除转换失败的行
ds_others['月份'] = ds_others['时间'].dt.month  

result = ds.groupby(["时间", "模型"])["访问次数"].sum().reset_index() #：对一日内同一API的访问次数进行统计
result_other = ds_others.groupby(["月份","模型"])["访问次数"].sum().reset_index()#：按月份进行统计

l_result = result.pivot(index="时间", columns="模型", values="访问次数").fillna(0)
l_result_month = result_other.pivot(index="月份",columns="模型",values="访问次数").fillna(0)
# 直接保存为CSV
l_result.to_csv("apiperday.csv")
l_result_month.to_csv("apipermonth.csv")



# 读取处理后的CSV文件
df = pd.read_csv("apiperday.csv")
df = df.astype(str)
# 转换为ECharts所需的JSON格式
data_json = df.to_dict(orient="records")

# 保存为JSON文件
with open("apiperday.json", "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

# 读取处理后的CSV文件
dm = pd.read_csv("apipermonth.csv")
dm = dm.astype(str)
# 转换为ECharts所需的JSON格式
data_json = dm.to_dict(orient="records")

# 保存为JSON文件
with open("apipermonth.json", "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)
