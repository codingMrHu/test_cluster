## 利用brich实现文本层次聚类,将文本内容分类

- 1.输入数据如下：

![Image text](https://github.com/codingMrHu/test_cluster/blob/master/image/data.png)



- 2.运行结果如下,聚类前数据有9条 聚类后6条;

字典key为类别，value是表示同一类别的index(text.dat中的行,从0开始) {0: [0, 1, 2], 1: [3, 4], 2: [5], 3: [6], 4: [7], 5: [8]}
0,1,2被聚为一类 输出了该类的中心点"吴亦凡陈伟霆“互怼“酷狗赛道TOP1学员压轴来袭"。

修改Birch(threshold=0.7,n_clusters=None)中的threshold参数可调整聚类效果

![Image text](https://github.com/codingMrHu/test_cluster/blob/master/image/result.png)
