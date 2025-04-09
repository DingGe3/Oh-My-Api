import pandas as pd
import json
import os
from datetime import datetime
from excel_to_csv import excel_to_csv  # 自定义模块
from pathlib import Path

class AccessDataAnalyzer:
    def __init__(self, excel_path="data.xlsx", csv_path="data.csv", output_dir=None, target_month=3, target_day=1, year="2025"):
        self.excel_path = excel_path
        self.csv_path = csv_path
        # 设置默认输出路径为脚本所在目录的上一级目录下的output文件夹
        if output_dir is None:
            script_dir = Path(__file__).resolve().parent
            parent_dir = script_dir.parent
            self.output_dir = parent_dir / 'data_processed'
        else:
            self.output_dir = output_dir
        self.target_month = target_month
        self.target_day = target_day
        self.year = year

    def setup_working_directory(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print("当前工作目录:", os.getcwd())

    def convert_excel_to_csv(self):
        excel_to_csv(self.excel_path, self.csv_path)

    def process_data(self):
        date_format = "%Y-%m-%d"
        target_date = pd.to_datetime(f"{self.year}-{self.target_month:02d}-{self.target_day:02d}", format=date_format)

        reader = pd.read_csv(self.csv_path, encoding="utf-8-sig", iterator=True, chunksize=1000)
        filtered_chunks, other_chunks = [], []

        for chunk in reader:
            chunk["日期"] = pd.to_datetime(
                f"{self.year}-" + chunk["时间"].str[:5],
                format=date_format,
                errors="coerce"
            )
            filtered = chunk[(chunk["日期"].dt.month == self.target_month) & (chunk["日期"] >= target_date)]
            others = chunk[chunk["日期"].dt.month != self.target_month]
            filtered_chunks.append(filtered)
            other_chunks.append(others)

        df_filtered = pd.concat(filtered_chunks, ignore_index=True)
        df_others = pd.concat(other_chunks, ignore_index=True)

        for df in [df_filtered, df_others]:
            df["访问次数"] = 1

        df_filtered["时间"] = pd.to_datetime(df_filtered["时间"].str.split(" ").str[0], format="%m-%d", errors="coerce")
        df_filtered["时间"] = df_filtered["时间"].dt.strftime("%m-%d")

        current_year = str(datetime.now().year)
        df_others["时间"] = pd.to_datetime(
            current_year + '-' + df_others["时间"].astype(str).str.strip(),
            format='%Y-%m-%d %H:%M:%S',
            errors='coerce'
        )
        df_others = df_others.dropna(subset=["时间"])
        df_others["月份"] = df_others["时间"].dt.month

        return df_filtered, df_others

    def aggregate_and_save(self, df_filtered, df_others):
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        def pivot_and_save(df, index, columns, file_prefix):
            result = df.groupby([index, columns])["访问次数"].sum().reset_index()
            pivot_table = result.pivot(index=index, columns=columns, values="访问次数").fillna(0)

            csv_file = os.path.join(self.output_dir, f"{file_prefix}.csv")
            json_file = os.path.join(self.output_dir, f"{file_prefix}.json")

            pivot_table.to_csv(csv_file)
            self.save_to_json(csv_file, json_file)

        pivot_and_save(df_filtered, "时间", "模型", "apiperday")
        pivot_and_save(df_others, "月份", "模型", "apipermonth")
        pivot_and_save(df_filtered, "时间", "IP", "ipperday")
        pivot_and_save(df_others, "月份", "IP", "ippermonth")

    def save_to_json(self, csv_path, json_path):
        df = pd.read_csv(csv_path).astype(str)
        data_json = df.to_dict(orient="records")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)

    def run(self):
        self.setup_working_directory()
        self.convert_excel_to_csv()
        df_filtered, df_others = self.process_data()
        print(f"目标月份数据：{len(df_filtered)} 行，其他月份数据：{len(df_others)} 行")
        self.aggregate_and_save(df_filtered, df_others)
