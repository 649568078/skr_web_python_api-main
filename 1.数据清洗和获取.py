""" MTI interactive """
import argparse
import os
import sys
import time

from skr_web_api import Submission, SEMREP_INTERACTIVE_URL
import pandas as pd
import re
import json
import spacy
import pickle
import pymysql
import time

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
    # stopwords = json.load(open('./stopwords-en.json', 'rb'))
    pattern = re.compile('^[a-z0-9\.\(\)_]+$')
    for doc in docs:
        doc = nlp(doc)
        this_data = {
            'words': [],
            'spacy_stopwords': [],
            'digit': [],
            'punct': [],
            'space': [],
            'num': [],
            'url': [],
            'email': [],
            'my_stopwords': [],
            'length': [],
            'pattern': [],
            'pos': [],
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
            # 单词的粗粒度的词性标注，如名词、动词、形容词等。
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
    selected_column_by_name = df["Title_replace"]  # 替换为你的列名
    # 通过列索引选择列
    selected_column_by_index = df.iloc[:, 1]  # 替换为你的列索引，这里选择第2列（索引为1）
    # 打印选定的列
    print("Selected Column by Name:")
    print(selected_column_by_name)
    docs = selected_column_by_name.tolist()
    file_name = 'my_list.pkl'
    # 检查文件是否存在
    if not os.path.exists(file_name):
        # 保存列表到文件
        with open(file_name, 'wb') as file:
            pickle.dump(docs, file)
        print(f"列表已保存到 {file_name}")
    else:
        # 从文件加载列表
        with open(file_name, 'rb') as file:
            docs = pickle.load(file)
        print(f"从 {file_name} 加载的列表:", docs)
    str_text = ""
    count = 0
    for doc in docs:
        str_text += doc + "\n"
        if count == 10:
            inputtext_list.append(str_text)
            str_text = ""
            count = 0
        count += 1
    inputtext_list.append(str_text)
    return inputtext_list


def simple_process_mysql():
    # 读取 Excel 文件
    inputtext_list = []
    excel_file = r"C:\Users\Administrator\PycharmProjects\skr_web_python_api-main\12_14_2023-所有资助项目指南.xlsx"  # 替换为你的 Excel 文件路径
    df = pd.read_excel(excel_file)
    # 选择特定列，可以使用列名或列索引
    # 通过列名选择列
    selected_column_by_name = df["Title_replace"]  # 替换为你的列名
    # 通过列索引选择列
    selected_column_by_index = df.iloc[:, 1]  # 替换为你的列索引，这里选择第2列（索引为1）
    # 打印选定的列
    print("Selected Column by Name:")
    print(selected_column_by_name)
    docs = selected_column_by_name.tolist()

    str_text = ""
    count = 1
    id = 1
    for doc in docs:
        str_text += doc + "\n"
        if count == 10:
            insert_query = "INSERT INTO nihguide3 (title,id) VALUES (%s,%s)"
            try:
                # 执行插入操作
                cursor.execute(insert_query, (str_text,id))
                # 提交事务
                connection.commit()
                print("插入操作成功！")
            except Exception as e:
                # 发生错误时回滚
                connection.rollback()
                print(f"插入操作失败: {e}")
            str_text = ""
            count = 1
            id += 1
        count += 1

    insert_query = "INSERT INTO nihguide3 (title,id) VALUES (%s,%s)"
    try:
        # 执行插入操作
        cursor.execute(insert_query, (str_text, id))
        # 提交事务
        connection.commit()
        print("插入操作成功！")
    except Exception as e:
        # 发生错误时回滚
        connection.rollback()
        print(f"插入操作失败: {e}")
    return


if __name__ == '__main__':

    # excel_process()
    # inputtext_list = simple_process()

    # inputtext = "NIDA REI Academic Research Enhancement Award AREA Training a Diverse Data Science Workforce for Addiction Research R15 Clinical Trial Not Allowed"

    # 数据库连接参数
    host = 'localhost'  # 替换为您的MySQL主机地址
    user = 'root'  # 替换为您的MySQL用户名
    password = 'xx19941130'  # 替换为您的MySQL密码
    database = 'nih'  # 替换为您的MySQL数据库名
    # 连接到MySQL数据库
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    # 创建游标对象
    cursor = connection.cursor()


    #simple_process_mysql()  # 用mysql创建10个一组的title集合

    #查询数据库中的空数据
    select_query = "SELECT id,title FROM nihguide3 WHERE mark IS NULL"
    cursor.execute(select_query)
    inputtext_list = cursor.fetchall()

    # 从数据库调出程序
    for inputtext in inputtext_list:
        time.sleep(5)
        id = inputtext[0]
        title = inputtext[1]
        print([id,title])
        II_SKR_SERVERURL = 'https://ii.nlm.nih.gov/cgi-bin/II/UTS_Required'
        MTI_INTERACTIVE_URL = II_SKR_SERVERURL + "/API_MTI_interactive.pl"
        email = "judayeshou@judayeshou@gmail.com"
        apikey = "2b4b6064-21bd-40ca-b4ff-719c322cdf91"
        inst = Submission(email, apikey)
        serviceurl = ""
        if serviceurl != "":
            inst.set_serviceurl(serviceurl)
        inst.init_mti_interactive(title, args='-opt1L_DCMS')
        response = inst.submit()
        print(f"开始更新{id}")
        update_query = f"UPDATE nihguide3 SET mesh = '{response.text}' WHERE id = '{id}'"
        update_query2 = f"UPDATE nihguide3 SET mark = '1' WHERE id = '{id}'"
        try:
            cursor.execute(update_query)
            cursor.execute(update_query2)
            # 提交事务
            connection.commit()
            print("更新操作成功！")
        except Exception as e:
            # 发生错误时回滚
            connection.rollback()
            print(f"更新操作失败: {e}")

    # 关闭游标和连接
    cursor.close()
    connection.close()
