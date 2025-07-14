import pandas as pd
from datetime import datetime
import json
import os
from sqlalchemy import create_engine

class ModelAccessJsonGenerator:
    def __init__(self,
                 db_url="mysql+pymysql://root:123456@localhost:3306/ohmyapi?charset=utf8mb4",
                 output_folder="data_processed",
                 output_filename="deepseekday.json",
                 table_name="access_logs"):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.output_folder = output_folder
        self.output_filename = output_filename
        self.table_name = table_name

        self.df = None
        self.result_df = None

        # 构造输出路径：上一级目录/output/文件名
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.output_path = os.path.join(parent_dir, output_folder, output_filename)

        # 确保目录存在
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def load_data(self):
        # 假设你的数据库表有 utc_date 字段和 model 字段
        sql = f"SELECT utc_date, model FROM {self.table_name}"
        try:
            self.df = pd.read_sql(sql, self.engine)
            self.df['访问次数'] = 1
            print(f"已从数据库读取数据，共 {len(self.df)} 条记录。")
        except Exception as e:
            print("读取数据库失败：", e)
            self.df = pd.DataFrame()

    def aggregate_data(self):
        grouped = self.df.groupby(["utc_date", "model"])["访问次数"].sum().reset_index()
        pivot_df = grouped.pivot(index="utc_date", columns="model", values="访问次数").fillna(0).astype(str)
        self.result_df = pivot_df.reset_index()
        print("数据已按日期和模型汇总。")

    def format_dates(self):
        # 这里保留完整日期格式：YYYY-MM-DD
        self.result_df['时间'] = self.result_df['utc_date'].apply(
            lambda x: x.strftime("%Y-%m-%d")
        )

        self.result_df.drop(columns=['utc_date'], inplace=True)
        cols = ['时间'] + [col for col in self.result_df.columns if col != '时间']
        self.result_df = self.result_df[cols]
        print("日期已格式化为 YYYY-MM-DD。")

    def export_json(self):
        data = self.result_df.to_dict(orient='records')
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存 JSON 文件：{self.output_path}")

    def run(self):
        self.load_data()
        if not self.df.empty:
            self.aggregate_data()
            self.format_dates()
            self.export_json()
