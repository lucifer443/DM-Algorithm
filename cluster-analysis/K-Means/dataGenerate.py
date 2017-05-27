import random

# 生成2D随机数据
def data_gen(mid, rad, total):
    result = []
    for i in range(total):
        result.append((random.uniform(mid[0]-rad, mid[0]+rad), random.uniform(mid[1]-rad, mid[1]+rad)))
    return result
