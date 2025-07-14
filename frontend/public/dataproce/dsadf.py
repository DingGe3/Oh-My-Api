import pandas as pd

df = pd.read_csv(r'C:\Users\Administrator\Desktop\Oh-My-Api-DingGe3-vue-version\frontend\public\dataproce\data.csv')


def add_year(row_index, datetime_str):
    if pd.isna(datetime_str):
        return datetime_str
    year = 2025 if 2 <= row_index <= 1367 else 2024
    # datetime_str 形如 "MM-DD HH:MM:SS"
    date_part, time_part = datetime_str.split(' ')
    month, day = date_part.split('-')
    month = month.zfill(2)
    day = day.zfill(2)
    return f"{year}-{month}-{day} {time_part}"

df['时间'] = [add_year(idx+1, dt) for idx, dt in enumerate(df['时间'])]

df.to_csv('data_with_year.csv', index=False)
