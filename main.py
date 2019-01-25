# coding=utf-8
import sys
import jieba
import numpy as np
from sklearn import feature_extraction    
from sklearn.feature_extraction.text import TfidfTransformer    
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import Birch
reload(sys)  
sys.setdefaultencoding('utf-8')

class Cluster():
    def init_data(self):
        # corpus = [] #文档预料 空格连接
        corpus = []
        # f_write = open("jieba_result.dat","w")
        self.title_dict = {}
        with open('text.dat','r') as f:
            index = 0
            for line in f:
                title = line.strip()
                self.title_dict[index] = title
                seglist = jieba.cut(title,cut_all=False)  #精确模式  
                output = ' '.join(['%s'%x for x in list(seglist)]).encode('utf-8')       #空格拼接
                # print index,output
                index +=1
                corpus.append(output.strip())

        #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频  
        vectorizer = CountVectorizer()  
        #该类会统计每个词语的tf-idf权值  
        transformer = TfidfTransformer()  
        #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  
        #获取词袋模型中的所有词语    
        word = vectorizer.get_feature_names()
        #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重  
        self.weight = tfidf.toarray()
        # print self.weight

    def birch_cluster(self):
        print ('start cluster Birch -------------------' )
        self.cluster = Birch(threshold=0.6,n_clusters=None)
        self.cluster.fit_predict(self.weight)

        
    def get_title(self):
        # self.cluster.labels_ 为聚类后corpus中文本index 对应 类别 {index: 类别} 类别值int值 相同值代表同一类
        cluster_dict = {}
        # cluster_dict key为Birch聚类后的每个类，value为 title对应的index
        for index,value in enumerate(self.cluster.labels_):
            if value not in cluster_dict:
                cluster_dict[value] = [index]
            else:
                cluster_dict[value].append(index)
        print cluster_dict

        print ("-----before cluster Birch count title:",len(self.title_dict))
        # result_dict key为Birch聚类后距离中心点最近的title，value为sum_similar求和
        
        result_dict = {}
        for indexs in cluster_dict.values():
            latest_index = indexs[0]
            similar_num = len(indexs)
            if len(indexs)>=2:
                min_s = np.sqrt(np.sum(np.square(self.weight[indexs[0]]-self.cluster.subcluster_centers_[self.cluster.labels_[indexs[0]]])))
                for index in indexs:
                    s = np.sqrt(np.sum(np.square(self.weight[index]-self.cluster.subcluster_centers_[self.cluster.labels_[index]])))
                    if s<min_s:
                        min_s = s
                        latest_index = index

            title = self.title_dict[latest_index]

            result_dict[title] = similar_num
        print ("-----after cluster Birch count title:",len(result_dict))
        for title in result_dict:
            print title,result_dict[title]
        return result_dict
    
    def run(self):
        self.init_data()
        self.birch_cluster()
        self.get_title()

if __name__=='__main__':
    cluster = Cluster()
    cluster.run()
