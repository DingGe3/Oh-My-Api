import pandas as pd

def excel_to_csv(excel_path, csv_path, sheet_name=0):
    """
    将Excel文件转换为CSV文件。

    """
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)  # 读取Excel
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # 保存为CSV
        print(f"转换成功: {csv_path}")
    except Exception as e:
        print(f"转换失败: {e}")