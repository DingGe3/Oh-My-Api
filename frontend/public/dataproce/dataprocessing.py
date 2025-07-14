import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine

class AccessDataAnalyzer:
    def __init__(self,
                 db_url="mysql+pymysql://root:123456@localhost:3306/ohmyapi?charset=utf8mb4",
                 output_dir=None,
                 target_month=3,
                 target_day=1,
                 year="2025"):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)

        # 设置默认输出路径为脚本所在目录的上一级目录下的 data_processed 文件夹
        if output_dir is None:
            script_dir = Path(__file__).resolve().parent
            parent_dir = script_dir.parent
            self.output_dir = parent_dir / 'data_processed'
        else:
            self.output_dir = Path(output_dir)

        self.target_month = target_month
        self.target_day = target_day
        self.year = year

    def process_data(self):
    # 读取数据
        sql = "SELECT 时间, 模型, IP FROM dataofapi"
        df_all = pd.read_sql(sql, self.engine)

        # 统一解析为 datetime（现在时间格式应为 yyyy-mm-dd hh:mm:ss）
        df_all["时间"] = pd.to_datetime(df_all["时间"], errors="coerce")

        # 创建日期列（带年）
        df_all["日期"] = df_all["时间"].dt.date

        # 构造目标起始日期（例如 2025-03-01）
        target_date = datetime.strptime(f"{self.year}-{self.target_month:02d}-{self.target_day:02d}", "%Y-%m-%d").date()

        # 分离目标月数据（从目标日开始）
        df_filtered = df_all[
            (df_all["时间"].dt.month == self.target_month) &
            (df_all["日期"] >= target_date)
        ].copy()

        # 其他月的数据
        df_others = df_all[df_all["时间"].dt.month != self.target_month].copy()

        # 添加访问次数
        for df in [df_filtered, df_others]:
            df["访问次数"] = 1

        # 目标月保留“完整年月日”
        df_filtered["时间"] = df_filtered["时间"].dt.strftime("%Y-%m-%d")

        # 其他月保留“完整年月”
        df_others["月份"] = df_others["时间"].dt.strftime("%Y-%m")

        return df_filtered, df_others


    def aggregate_and_save(self, df_filtered, df_others):
        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        def pivot_and_save(df, index, columns, file_prefix):
            result = df.groupby([index, columns])["访问次数"].sum().reset_index()
            pivot_table = result.pivot(index=index, columns=columns, values="访问次数").fillna(0)

            csv_file = self.output_dir / f"{file_prefix}.csv"
            json_file = self.output_dir / f"{file_prefix}.json"

            pivot_table.to_csv(csv_file, encoding="utf-8-sig")
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
        df_filtered, df_others = self.process_data()
        print(f"目标月份数据：{len(df_filtered)} 行，其他月份数据：{len(df_others)} 行")
        self.aggregate_and_save(df_filtered, df_others)