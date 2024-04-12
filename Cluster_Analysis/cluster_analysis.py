import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
import jieba
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')


# 中文分词的函数
def chinese_word_cut(mytext):
    # 文本预处理 ：去除一些无用的字符只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
    new_data = " ".join(new_data)

    # 文本分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    result_list = []
    path = os.getcwd()
    # 加载停用词库
    with open(os.path.join(path, "停用词库.txt"), encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
        stop_words = set()
        for i in f.readlines():
            stop_words.add(i.replace("\n", ""))  # 去掉读取每一行数据的\n
    # 去除停用词
    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    return " ".join(result_list)



def dim_reduction_stand(mytext, dim = 1000):
    # 对分词结果进行词向量化并降维到1000维同时进行标准化操作

    vectorizer = CountVectorizer()
    svd = TruncatedSVD(dim)  # 降到1000维
    normalizer = Normalizer(copy=False)  # 标准化
    lsa = make_pipeline(svd, normalizer)
    x = lsa.fit_transform(vectorizer.fit_transform(mytext))
    return x


def get_kw_weight(mytext):
    # 使用TF-IDF提权关键词并获取权重

    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(mytext)
    tfidf_weight = tfidf.toarray()

    return tfidf_weight


def kmeans_visual(tfidf_weight,n):
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(tfidf_weight)

    # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(tfidf_weight)

    # x = []
    # y = []
    #
    # for i in decomposition_data:
    #
    #     x.append(i[0])
    #     y.append(i[1])

    data = decomposition_data.tolist()
    return data




def analysis(mytext, n):
    data = pd.read_csv(mytext)
    data['分词结果'] = data['评论内容'].apply(chinese_word_cut)
    x = dim_reduction_stand(data['分词结果'])
    weight = get_kw_weight(x)

    return kmeans_visual(weight,n)



if __name__ == '__main__':

    data2 = pd.read_csv('JD_comment.csv')
    data2.head()
    data2['分词结果'] = data2['评论内容'].apply(chinese_word_cut)

    kmeans_visual(get_kw_weight(dim_reduction_stand(data2['分词结果'])), 2)