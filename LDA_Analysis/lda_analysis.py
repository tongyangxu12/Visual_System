import pandas as pd
import os
import re
import jieba
import tomotopy as tp
import matplotlib.pyplot as plt
import pyLDAvis
import numpy as np

import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号



def preprocessing(mytext):
    mytext.drop_duplicates(inplace=True)  # 删除重复数据
    mytext.reset_index(drop=True, inplace=True)
    index_list = []
    for index, value in enumerate(mytext["评论内容"]):
        if len(value) < 10:
            index_list.append(index)
    print(len(index_list))
    mytext.drop(index=index_list, inplace=True)
    return mytext


def chinese_word_cut(mytext):
    # 文本预处理 ：去除一些无用的字符只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
    new_data = " ".join(new_data)

    # 文本分词
    seg_list_exact = jieba.cut(new_data)
    result_list = []
    path = os.getcwd()
    # 加载停用词库
    with open(os.path.join(path, "停用词库.txt"), encoding='utf-8') as f: # 可根据需要打开停用词库，然后加上不想显示的词语
        con = f.readlines()
        stop_words = set()
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)

    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    return " ".join(result_list)


def find_k(docs, min_k=1, max_k=20, min_df=2):
    # min_df 词语最少出现在2个文档中

    scores = []
    for k in range(min_k, max_k):
        mdl = tp.LDAModel(min_df=min_df, k=k, seed=555)
        for words in docs:
            if words:
                mdl.add_doc(words)
        mdl.train(20)
        coh = tp.coherence.Coherence(mdl)
        scores.append(coh.get_score())


    # plt.plot(range(min_k, max_k), scores)
    # plt.xlabel("主题数量")
    # plt.ylabel("连贯性")
    # plt.show()

    return range(min_k, max_k), scores


def lda_visual(mytext, k):
    data = pd.read_csv(mytext)
    data = preprocessing(data)
    data["content_cutted"] = data["评论内容"].apply(chinese_word_cut)

    # 初始化LDA
    mdl = tp.LDAModel(k=k, min_df=2, seed=555)
    for words in data["content_cutted"]:
        # 确认words 是 非空词语列表
        if words:
            mdl.add_doc(words=words.split())

    # 训 练
    mdl.train()

    # 获取pyldavis需要的参数
    topic_term_dists = np.stack([mdl.get_topic_word_dist(k) for k in range(mdl.k)])
    doc_topic_dists = np.stack([doc.get_topic_dist() for doc in mdl.docs])
    doc_topic_dists /= doc_topic_dists.sum(axis=1, keepdims=True)
    doc_lengths = np.array([len(doc.words) for doc in mdl.docs])
    vocab = list(mdl.used_vocabs)
    term_frequency = mdl.used_vocab_freq

    prepared_data = pyLDAvis.prepare(
        topic_term_dists,
        doc_topic_dists,
        doc_lengths,
        vocab,
        term_frequency,
        start_index=0,  # tomotopy话题id从0开始，pyLDAvis话题id从1开始
        sort_topics=False  # 注意：否则pyLDAvis与tomotopy内的话题无法一一对应。
    )

    # pyLDAvis.show(prepared_data, ip='127.0.0.1', port=8888, n_retries=50,
    #      local=False, open_browser=True)
    # 可视化结果存到html文件中
    pyLDAvis.save_html(prepared_data, r'E:\Visual_System\app01\templates\ldavis.html')


def analysis_find_k(mytext):
    data = pd.read_csv(mytext)
    data = preprocessing(data)
    data["content_cutted"] = data["评论内容"].apply(chinese_word_cut)

    return find_k(docs=data['content_cutted'], min_k=1, max_k=10, min_df=2)



if __name__ == '__main__':
    # data3 = pd.read_csv('JD_comment.csv')
    # data3 = preprocessing(data3)
    # data3["content_cutted"] = data3["评论内容"].apply(chinese_word_cut)
    BASE_DIR = os.getcwd()
    print(BASE_DIR)