import re
import pandas

str_data = """
|CONTINUED DEVELOPMENT AND MAINTENANCE OF BIOINFORMATICS AND COMPUTATIONAL BIOLOGY SOFTWARE|
|PREDOCTORAL TRAINING IN BIOINFORMATICS AND COMPUTATIONAL BIOLOGY|
|Notice of Special Interest : Administrative Supplements to Support Collaborations to Improve the AI/ML-Readiness of NIH-Supported Data|
|Notice of Special Interest : Administrative Supplements to Support Collaborations to Improve the AI/ML-Readiness of NIH-Supported Data|
|Notice of Special Interest : Administrative Supplements to Support Collaborations to Improve the AI/ML-Readiness of NIH-Supported Data|
|Bioinformatics Resource Centers  for Infectious Diseases|
|Notice of Special Interest: Advanced Computational Approaches to Elucidate Disease Pathology and Identify Novel Therapeutics for Addiction|
|Investigator Initiated Research in Computational Genomics and Data Science|
|Investigator Initiated Research in Computational Genomics and Data Science|
|Notice of Special Interest : Administrative Supplements for Workforce Development at the Interface of Information Sciences, Artificial Intelligence and Machine Learning , and Biomedical Sciences|
"""

text ="""00000000|*Artificial Intelligence|D001185|6820|MH|RtM via: Artificial Intelligence;Forced Lookup:artificial intelligence|TI|MM;RC|1050^23^0;258^2^0;395^2^0;532^2^0
00000000|Data Science|D000077488|1090|MH|RtM via: Data Science;Forced Leaf Node Lookup:data sciences|TI|MM|834^12^0;911^12^0
00000000|Computational Biology|D019295|4119|MH|RtM via: Bio-Informatics;RtM via: Computational Biology;Forced Non-Leaf Node Lookup:computational biology|TI|MM;RC|42^14^0;572^14^0;61^21^0;137^21^0;118^14^0
00000000|Genomics|D023281|3984|MH|RtM via: Genomics;Forced Non-Leaf Node Lookup:genomics|TI|MM;RC|821^8^0;898^8^0
00000000|Software|D012984|2667|MH|RtM via: Computer software;Forced Non-Leaf Node Lookup:software|TI|MM;RC|83^8^0
00000000|Machine Learning|D000069550|2214|MH|RtM via: Machine Learning;Forced Non-Leaf Node Lookup:machine learning|TI|MM;RC|1078^16^0
00000000|Workforce|D000078329|1000|MH|Forced Non-Leaf Node Lookup:workforces||MM|986^9^0
"""
# 定义不确定的区间列表
intervals = []
#使用正则表达式找到每个分隔符之后的第一个数据及其位置
pattern = r'\|([^|]+)\|'
matches = re.finditer(pattern, str_data)
# 输出每个分隔符之后的第一个数据及其位置
for match in matches:
    data = match.group(1).strip()
    start_position = match.start(1)
    end_position = match.end(1)
    print(f"数据: {data}, 起始位置: {start_position}, 结束位置: {end_position}")
    intervals.append((start_position,end_position))

print(intervals)
# 使用enumerate给列表加上索引
indexed_intervals = list(enumerate(intervals))
#识别每一条term，归属每个位置属于哪个区间

# 使用正则表达式匹配末尾的数字
text_list = text.split('\n')
print(text_list)
# 初始化字典，每个键对应一个空列表

my_dict = {f'key_{i}': [] for i in range(0, 10)}

for each_text in text_list:
    print(each_text)
    pattern = r'\d+\^\d+\^\d+'
    term_name = re.search("00000000\|(.*?)\|",each_text)
    if term_name != None:
        term_name = term_name.group(1)
        print(f"term_name是{term_name}")
        matches = re.findall(pattern, each_text)
        for match in matches:
            match = match.split("^")[0]
            print(match)
            # 判断随机数属于哪个区间
            for index, value in indexed_intervals:
                start, end = value
                if start <= int(match) <= end:
                    print(f"{term_name} {match} 属于区间 {start} 到 {end} 是第{index}段")
                    my_dict[f'key_{index}'].append(term_name)
                    break
print(my_dict)

