import pandas as pd
from datetime import datetime
import json
import os

class ModelAccessJsonGenerator:
    def __init__(self, csv_path, output_folder="data_processed", output_filename="deepseekday.json"):
        self.csv_path = csv_path
        self.output_folder = output_folder
        self.output_filename = output_filename
        self.df = None
        self.result_df = None

        # 构造输出路径：上一级目录/output/文件名
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.output_path = os.path.join(parent_dir, output_folder, output_filename)

        # 确保目录存在
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def load_data(self):
        self.df = pd.read_csv(self.csv_path)
        self.df['访问次数'] = 1
        print(f"已加载数据，共 {len(self.df)} 条记录。")

    def aggregate_data(self):
        grouped = self.df.groupby(["utc_date", "model"])["访问次数"].sum().reset_index()
        pivot_df = grouped.pivot(index="utc_date", columns="model", values="访问次数").fillna(0).astype(str)
        self.result_df = pivot_df.reset_index()
        print("数据已按日期和模型汇总。")

    def format_dates(self):
        self.result_df['时间'] = self.result_df['utc_date'].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%m-%d")
        )
        self.result_df.drop(columns=['utc_date'], inplace=True)
        cols = ['时间'] + [col for col in self.result_df.columns if col != '时间']
        self.result_df = self.result_df[cols]
        print("日期已格式化为 MM-DD 格式。")

    def export_json(self):
        data = self.result_df.to_dict(orient='records')
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存 JSON 文件：{self.output_path}")

    def run(self):
        self.load_data()
        self.aggregate_data()
        self.format_dates()
        self.export_json()
