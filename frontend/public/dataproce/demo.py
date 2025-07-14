import sys
sys.path.append('./dataproce')
from deepseek_processing import ModelAccessJsonGenerator
from dataprocessing import AccessDataAnalyzer

if __name__ == "__main__":
    analyzer = AccessDataAnalyzer(
        db_url="mysql+pymysql://root:123456@localhost:3306/ohmyapi?charset=utf8mb4",
        target_month=3,
        target_day=1,
        year="2025"
    )
    analyzer.run()


if __name__ == "__main__":
    generator = ModelAccessJsonGenerator(
        table_name="ds_data",  
        output_filename="deepseekday.json"
    )
    generator.run()
