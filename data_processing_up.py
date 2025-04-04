import pandas as pd
import json
import os
from datetime import datetime
from excel_to_csv import excel_to_csv  # 自定义模块：将 Excel 转换为 CSV

# 设置脚本运行时的工作目录为当前脚本所在的目录
def setup_working_directory():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print("当前工作目录:", os.getcwd())

# 将 data.xlsx 文件转换为 data.csv（确保后续统一使用 CSV 处理）
def convert_excel_to_csv():
    excel_to_csv("data.xlsx", "data.csv")

# 处理 CSV 数据，分离出目标日期之后的目标月份数据和其他月份数据
def process_data(file_path, target_month=3, target_day=1, default_year="2025"):
    date_format = "%Y-%m-%d"
    # 构造目标日期时间对象（如 2025-03-01）
    target_date = pd.to_datetime(f"{default_year}-{target_month:02d}-{target_day:02d}", format=date_format)

    # 使用分块方式读取 CSV，避免大文件内存占用过高
    reader = pd.read_csv(file_path, encoding="utf-8-sig", iterator=True, chunksize=1000)
    filtered_chunks, other_chunks = [], []

    for chunk in reader:
        # 取出“时间”字段的前五位（假设格式是 MM-DD hh:mm:ss），补全年份组成 YYYY-MM-DD
        chunk["日期"] = pd.to_datetime(
            f"{default_year}-" + chunk["时间"].str[:5], 
            format=date_format, 
            errors="coerce"  # 无效日期将转为 NaT
        )

        # 提取目标月份的日期数据（例：3月1日及之后的）
        filtered = chunk[(chunk["日期"].dt.month == target_month) & (chunk["日期"] >= target_date)]
        # 提取其他月份的数据
        others = chunk[chunk["日期"].dt.month != target_month]

        # 分别加入对应列表
        filtered_chunks.append(filtered)
        other_chunks.append(others)

    # 合并所有分块数据
    df_filtered = pd.concat(filtered_chunks, ignore_index=True)
    df_others = pd.concat(other_chunks, ignore_index=True)

    # 添加访问次数统计列（每条记录算一次访问）
    for df in [df_filtered, df_others]:
        df['访问次数'] = 1

    # 统一格式化：目标月份数据的时间字段只保留 MM-DD
    df_filtered['时间'] = pd.to_datetime(df_filtered['时间'].str.split(' ').str[0], format='%m-%d', errors='coerce')
    df_filtered['时间'] = df_filtered['时间'].dt.strftime('%m-%d')  # 格式化为字符串：03-01、03-02 等

    # 处理其他月份数据，转换“时间”字段为完整 datetime（假设格式是 YYYY-MM-DD hh:mm:ss）
    current_year = str(datetime.now().year)
    df_others['时间'] = pd.to_datetime(
        current_year + '-' + df_others['时间'].astype(str).str.strip(),
        format='%Y-%m-%d %H:%M:%S',
        errors='coerce'
    )
    df_others = df_others.dropna(subset=["时间"])  # 去除转换失败的行
    df_others['月份'] = df_others['时间'].dt.month  # 提取月份字段

    return df_filtered, df_others

# 对数据进行统计聚合并保存为 CSV + JSON（支持 API 和 IP 的按天/月分析）
def aggregate_and_save(df_filtered, df_others):
    def pivot_and_save(df, index, columns, file_name_prefix):
        # 分组统计访问次数
        result = df.groupby([index, columns])["访问次数"].sum().reset_index()

        # 生成透视表，以便用于图表
        pivot_table = result.pivot(index=index, columns=columns, values="访问次数").fillna(0)

        # 保存 CSV
        csv_file = f"{file_name_prefix}.csv"
        json_file = f"{file_name_prefix}.json"
        pivot_table.to_csv(csv_file)

        # 另存为 ECharts 使用的 JSON 格式
        save_to_json(csv_file, json_file)

    # 各类分析的聚合保存（API维度 + IP维度，日维度 + 月维度）
    pivot_and_save(df_filtered, "时间", "模型", "apiperday")     # 每日每模型访问
    pivot_and_save(df_others, "月份", "模型", "apipermonth")    # 每月每模型访问
    pivot_and_save(df_filtered, "时间", "IP", "ipperday")       # 每日每IP访问
    pivot_and_save(df_others, "月份", "IP", "ippermonth")       # 每月每IP访问

# 将 CSV 文件转换为 JSON 文件（用于 ECharts 图表渲染）
def save_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path).astype(str)  # 全部转换为字符串，避免类型不兼容
    data_json = df.to_dict(orient="records")  # 转换为列表字典结构
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)  # 写入 JSON 文件

# 主流程
def main():
    setup_working_directory()       # 确保运行目录一致
    convert_excel_to_csv()          # 先转换 Excel 为 CSV
    df_filtered, df_others = process_data("data.csv")  # 数据预处理与分类
    print(f"目标月份数据：{len(df_filtered)} 行，其他月份数据：{len(df_others)} 行")
    aggregate_and_save(df_filtered, df_others)  # 聚合并保存结果

# 程序入口
if __name__ == "__main__":
    main()
