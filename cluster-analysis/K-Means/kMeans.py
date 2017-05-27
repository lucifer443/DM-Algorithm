import random
from dataGenerate import data_gen


# 计算相异性，这采用了欧式距离
def dissimilarity(x,y):
    return (sum([(x[i]-y[i])**2 for i in range(len(x))]))**0.5


# 由簇计算中心
def cal_center(cluster):
    result = []
    dim = len(cluster[0])
    l = len(cluster)
    for d in range(dim):
        result.append(sum([c[d] for c in cluster])/l)
    return tuple(result)


# K-Mean，返回中心和簇
def k_mean(data_set, k):
    elem_dict = {}.fromkeys(data_set, 0)
    center = random.sample(data_set, k)
    clusters = [[] for i in range(k)]
    for k in elem_dict:
        clusters[elem_dict[k]].append(k)
    flag = True  # 标志位，用来判断是否终止迭代
    count = 1
    while flag:
        print('第%d次迭代'% count, [len(i) for i in clusters], center)
        count += 1
        flag = False
        for data in data_set:
            dis = []
            for c in center:
                dis.append(dissimilarity(data, c))
                m = dis.index(min(dis))
            if elem_dict[data] != m:  # 分类情况变动时更新簇
                flag = True
                clusters[elem_dict[data]].pop(clusters[elem_dict[data]].index(data))
                clusters[m].append(data)
                elem_dict[data] = m
        center = [cal_center(i) for i in clusters]
    return center, clusters


if __name__ == '__main__':
    data = data_gen((10,15), 5, 100) + data_gen((40,50) ,10, 200) + data_gen((201,22), 30, 100)
    c,_ = k_mean(data, 3)
    print(c)

