import collections
import pandas as pd
import numpy as np
import stylecloud
import os
import re
import jieba
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def analysis(csv_data):

    # 读取数据集中的数据
    data = pd.read_csv(csv_data)


    # 对数据进行预处理，剔除重复值，由于是爬取到的商品评论数据，所以无需进行填充缺失值
    data = data.drop_duplicates()

    # 开始进行情感分析，使用snownlp
    # 遍历每条评论进行预测
    values = [SnowNLP(i).sentiments for i in data["评论内容"]]
    # 输出积极的概率，大于0.5的为积极，小于0.5的为消极
    # myval保存预测值
    myval = []
    good = 0
    mid = 0
    bad = 0
    for i in values:
        if i >= 0.6:
            myval.append("积极")
            good += 1
        elif 0.2 < i < 0.6:
            myval.append("中性")
            mid += 1
        else:
            myval.append("消极")
            bad += 1
    data["预测值"] = values
    data["评论类别"] = myval
    # print(data.head())

    # 经过了上面的打分操作，现在已经有了每句话都情感分值及其情感类别。
    # 接下来对情感分值和类别进行可视化展示
    rate = good / (good + bad + mid)
    rate *= 100

    # print(type(values))
    # print(len(values))

    y = data["评论类别"].value_counts().values.tolist()
    # print(type(y))
    # print(y)

    result1 = draw_WorldCloud(data[data["评论类别"]=="积极"]["评论内容"], "积极情绪")
    result2 = draw_WorldCloud(data[data["评论类别"] == "中性"]["评论内容"], "中性情绪")
    result3 = draw_WorldCloud(data[data["评论类别"] == "消极"]["评论内容"], "消极情绪")

    keyword_list = []
    for key, value in result1[3].items():
        item_dict = {"name": key, "value": value}
        keyword_list.append(item_dict)


    return y, values, rate, result1, keyword_list



def draw_WorldCloud(df, pic_name, color="black"):
    # print(path)
    data = "".join([item for item in df])
    # 文本预处理：去除一些无用的字符只提取出中文出来
    new_data = re.findall("[\u4e00-\u9fa5]+", data, re.S)
    new_data = "".join(new_data)
    # 文本分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    result_list = []
    path = os.getcwd()
    # 加载停用词库
    with open(os.path.join(path, "停用词库.txt"), encoding='utf-8') as f: # 可根据需要打开停用词阵，然后加上不想显示的词语
        con = f.readlines()
        stop_words = set()
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)

    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    word_counts = collections.Counter(result_list)

    word_counts_dict = dict(word_counts)

    # 词频统计：获取前100最高频的词
    word_counts_top = word_counts.most_common(100)
    # with open(f"{pic_name}词频统计.txt", "w", encoding="utf-8") as f:
    #     for i in word_counts_top:
    #         f.write(str(i[0]))
    #         f.write("\t")
    #         f.write(str(i[1]))
    #         f.write("\n")
    # print(word_counts_top)
    x = [item[0] for item in word_counts_top[:10]]
    y = [item[1] for item in word_counts_top[:10]]
    title = f"{pic_name}Top10高频词"

    # print(type(word_counts_dict))
    # print(word_counts_dict)
    # return word_counts_dict

    return x, y, title, word_counts_dict

if __name__ == '__main__':
    # word_counts_dict =
    analysis("JD_comment.csv")
    # print(type(word_counts_dict))
    # print(word_counts_dict)
    #
    # keyword_list = []
    # for key, value in word_counts_dict.items():
    #     item_dict = {"name": key, "value": value}
    #     keyword_list.append(item_dict)
    #
    # print(type(keyword_list))
    # print(keyword_list)
