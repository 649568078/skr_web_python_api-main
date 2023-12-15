""" MTI interactive """
import argparse
import os
from skr_web_api import Submission, SEMREP_INTERACTIVE_URL
import pandas as pd
import re
import json
import spacy
import pickle

def excel_process():
    # 读取 Excel 文件
    excel_file = r"C:\Users\Administrator\PycharmProjects\skr_web_python_api-main\12_14_2023-所有资助项目指南.xlsx"  # 替换为你的 Excel 文件路径
    df = pd.read_excel(excel_file)
    # 选择特定列，可以使用列名或列索引
    # 通过列名选择列
    selected_column_by_name = df["Title"]  # 替换为你的列名
    # 通过列索引选择列
    selected_column_by_index = df.iloc[:, 1]  # 替换为你的列索引，这里选择第2列（索引为1）
    # 打印选定的列
    print("Selected Column by Name:")
    print(selected_column_by_name)
    docs = selected_column_by_name.tolist()
    nlp = spacy.load("en_core_web_lg")
    datas = []
    #stopwords = json.load(open('./stopwords-en.json', 'rb'))
    pattern = re.compile('^[a-z0-9\.\(\)_]+$')
    for doc in docs:
        doc = nlp(doc)
        this_data = {
            'words':[],
            'spacy_stopwords':[],
            'digit':[],
            'punct':[],
            'space':[],
            'num':[],
            'url':[],
            'email':[],
            'my_stopwords':[],
            'length':[],
            'pattern':[],
            'pos':[],
        }
        for token in doc:  # -> for token in nlp(text):
            # 1. SPACY STOPWORDS
            if token.is_stop:
                this_data['spacy_stopwords'].append(token.text)
            #         elif token.is_digit and (float(token.text) !=  float(int(float(token.text)))):
            #             this_data['digit'].append(token.text)
            # is_punct 文本标点
            elif token.is_punct:
                this_data['punct'].append(token.text)
            elif token.is_space:
                this_data['space'].append(token.text)
            #         elif token.like_num:
            #             this_data['num'].append(token.text)
            elif token.like_url:
                this_data['url'].append(token.text)
            elif token.like_email:
                this_data['email'].append(token.text)
            # 词干
            # elif token.lemma_ in stopwords:
            #     this_data['my_stopwords'].append(token.text)
            elif len(token.lemma_) < 3:
                this_data['length'].append(token.text)
            elif not re.match(pattern, token.lemma_):
                this_data['pattern'].append(token.text)
            #单词的粗粒度的词性标注，如名词、动词、形容词等。
            elif not token.pos_ in ['ADJ', 'NOUN', 'PROPN', 'VERB', 'NUM'] and token.lemma_ not in ['ncov_19']:
                this_data['pos'].append({token.text: token.pos_})
            else:
                this_data['words'].append(token.lemma_.lower())
        datas.append(this_data)
    df_words = pd.DataFrame(datas)
    print(df_words)
    # 定义 Excel 文件路径
    excel_file_path = "./output_file.xlsx"  # 替换为你想要保存的 Excel 文件路径
    # 将 DataFrame 写入 Excel 文件
    df_words.to_excel(excel_file_path, index=False)

def simple_process():
    # 读取 Excel 文件
    inputtext_list = []
    excel_file = r"C:\Users\Administrator\PycharmProjects\skr_web_python_api-main\12_14_2023-所有资助项目指南.xlsx"  # 替换为你的 Excel 文件路径
    df = pd.read_excel(excel_file)
    # 选择特定列，可以使用列名或列索引
    # 通过列名选择列
    selected_column_by_name = df["Title"]  # 替换为你的列名
    # 通过列索引选择列
    selected_column_by_index = df.iloc[:, 1]  # 替换为你的列索引，这里选择第2列（索引为1）
    # 打印选定的列
    print("Selected Column by Name:")
    print(selected_column_by_name)
    docs = selected_column_by_name.tolist()
    str_text = ""
    count = 0
    for doc in docs:
        str_text += doc+"\n"
        if count == 10:
            inputtext_list.append(str_text)
            str_text = ""
            count = 0
        count += 1
    inputtext_list.append(str_text)
    return inputtext_list


if __name__ == '__main__':

    #excel_process()

    #inputtext_list = simple_process()

    inputtext = """
    Administrative Supplements for Workforce Development at the Interface of Information Sciences Artificial Intelligence and Machine Learning AI ML and Biomedical Sciences
    """


    II_SKR_SERVERURL = 'https://ii.nlm.nih.gov/cgi-bin/II/UTS_Required'
    MTI_INTERACTIVE_URL = II_SKR_SERVERURL + "/API_MTI_interactive.pl"
    email = "judayeshou@judayeshou@gmail.com"
    apikey = "2b4b6064-21bd-40ca-b4ff-719c322cdf91"
    inst = Submission(email, apikey)
    serviceurl = ""
    if serviceurl != "":
        inst.set_serviceurl(serviceurl)
    inst.init_mti_interactive(inputtext, args='-opt1L_DCMS')
    response = inst.submit()
    with open("New_response.txt","a+",encoding="utf-8") as f:
        f.write('response status: {}'.format(response.status_code))
        f.write('content: {}'.format(response.content.decode()))
    print('response status: {}'.format(response.status_code))
    print('content: {}'.format(response.content.decode()))
