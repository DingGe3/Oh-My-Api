import pandas as pd
from datetime import datetime
import json

# 1. 读取原始 CSV 数据
df = pd.read_csv('amount-2025-4.csv')

# 2. 添加辅助列“访问次数”
df['访问次数'] = 1

# 3. 按日期和模型分组求和
result = df.groupby(["utc_date", "model"])["访问次数"].sum().reset_index()

# 4. 透视为以日期为行，模型为列的表格
pivot_df = result.pivot(index="utc_date", columns="model", values="访问次数").fillna(0)

# 5. 将访问次数转为字符串（与目标结构一致）
pivot_df = pivot_df.astype(str)

# 6. 重置索引，准备添加“时间”列
pivot_df = pivot_df.reset_index()

# 7. 格式化日期（只保留月-日）并重命名为“时间”
pivot_df['时间'] = pivot_df['utc_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%m-%d"))

# 8. 移除原始 utc_date 列
pivot_df = pivot_df.drop(columns=['utc_date'])

# 9. 调整列顺序，把“时间”放在第一列
cols = ['时间'] + [col for col in pivot_df.columns if col != '时间']
pivot_df = pivot_df[cols]

# 10. 转为列表形式（list of dicts）
result_list = pivot_df.to_dict(orient='records')

# 11. 写入 JSON 文件
with open('deepseekday.json', 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False, indent=2)