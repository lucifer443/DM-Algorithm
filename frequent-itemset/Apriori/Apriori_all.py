# -*- coding:utf-8 -*-
'''Apriori算法实现，包含所有频繁模式'''


# 生成频繁1项集
def create_one(data_set):
    result = []
    for item in data_set:
        for t in item:
            if t not in result:
                result.append(t)
    return [frozenset([i])for i in result]


# 支持度过滤
def support_filter(c, support, data_set):
    dict_c = dict()
    support = len(data_set) * support
    for item in data_set:
        for i in c:
            if i <= set(item):
                if dict_c.get(i):
                    dict_c[i] += 1
                else:
                    dict_c[i] = 1
    r = dict()
    for k in dict_c:
        if dict_c[k] >= support:
            r[k] = dict_c[k]
    return r


# 连接生成候选集CK
def connect(lk):
    l = len(lk)
    r = []
    for i in range(l):
        for j in range(i + 1, l):
            list_i = list(lk[i])
            list_j = list(lk[j])
            list_i.sort()
            list_j.sort()
            if list_i[:-1] == list_j[:-1] and list_i[-1] < list_j[-1]:
                r.append(frozenset(lk[i] | lk[j]))
    return r


# 获得所有频繁模式
def apriori(data_set, count, lk, support, frequent_model, support_data):
    print('Apriori算法第%d层' % count)
    if count == 1:
        l1 = support_filter(create_one(data_set), support, data_set)
        support_data.update(l1)
        l1 = [list(i)[0] for i in list(l1)]
        l1.sort()
        l1 = [frozenset([i]) for i in l1]
        frequent_model.append(l1)
        apriori(data_set, 2, l1, support, frequent_model, support_data)
    ck = connect(lk)
    lp = support_filter(ck, support, data_set)
    support_data.update(lp)
    if not len(lp):
        return None
    else:
        lp = list(lp)
        frequent_model.append(lp)
        apriori(data_set, count+1, lp, support, frequent_model, support_data)


if __name__ == '__main__':
    l_test1 = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    l_test2 = [[1, 2, 3], [2, 3, 4], [1, 2], [2, 5], [3, 4], [1, 5]]
    fm = []
    sd ={}
    apriori(data, 1, [], 1/3, fm, sd)
    print(fm)
