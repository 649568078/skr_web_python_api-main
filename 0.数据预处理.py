""" MTI interactive """
import argparse
import os
from skr_web_api import Submission, SEMREP_INTERACTIVE_URL
import pandas as pd
import re
import json
import spacy
import pickle
import re

def pretreatment():
    excel_file = r"C:\Users\Administrator\PycharmProjects\skr_web_python_api-main\12_14_2023-所有资助项目指南.xlsx"  # 替换为你的 Excel 文件路径
    df = pd.read_excel(excel_file)
    selected_column_by_name = df["Title"]  # 替换为你的列名
    selected_column_by_index = df.iloc[:, 1]  # 替换为你的列索引，这里选择第2列（索引为1）
    docs = selected_column_by_name.tolist()
    #print(docs)
    pattern = r'\([^)]*\)'
    new_docs= []
    for doc in docs:
        result = re.sub(pattern, '', doc)
        new_docs.append(result.strip())
    for i in new_docs:
        print(i)
    # 定义 Excel 文件路径
    excel_file_path = "./pretreatment_output_file.xlsx"  # 替换为你想要保存的 Excel 文件路径
    # 将 DataFrame 写入 Excel 文件
    df_words = pd.DataFrame(new_docs)
    df_words.to_excel(excel_file_path, index=False)

if __name__ == '__main__':
    pretreatment()
