import sys
sys.path.append('./dataproce')
from dataprocessing import AccessDataAnalyzer
from deepseek_processing import ModelAccessJsonGenerator
datad=ModelAccessJsonGenerator("amount-2025-4.csv")
datap=AccessDataAnalyzer(excel_path="data.xlsx",year="2025")
datap.run()
datad.run()