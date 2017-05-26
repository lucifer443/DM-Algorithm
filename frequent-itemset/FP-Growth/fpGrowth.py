class FpTreeNode():
    def __init__(self, name, count=0, parent=None):
        self.name = name
        self.count = count
        self.children = {}
        self.parent = parent
        self.node_link = None

    def inc(self, num):
        self.count += num

    def show(self, n=1):
        print("%s:%d" % (self.name, self.count))
        for c in self.children:
            print("     " * n, end='')
            self.children[c].show(n+1)


# 按照频率字典排序
def order_item(item, compare_dict):
    result = []
    for i in sorted(item):
        if i not in compare_dict.keys():
            continue
        if not result:
            result.append(i)
        else:
            for j in range(len(result)):
                if compare_dict[i][0] > compare_dict[result[j]][0]:
                    result.insert(j, i)
                    break
            else:
                result.append(i)
    return result


# 更新头表
def update_table(start_node, target_node):
    node = start_node
    while node.node_link is not None:
        node = node.node_link
    node.node_link = target_node


# 插入节点
def insert_child(parent_node, item, header_table, count):
    if not len(item):
        return None
    if parent_node.children.get(item[0]) is not None:
        child = parent_node.children[item[0]]
        child.inc(count)
    else:
        child = FpTreeNode(item[0], count, parent_node)
        parent_node.children[item[0]] = child
        if header_table[child.name][1] is not None:
            update_table(header_table[item[0]][1], child)
        else:
            header_table[child.name][1] = child
    if len(item) > 1:
        insert_child(child, item[1:], header_table, count)


# 创建FP树
def create_tree(data, support):
    temp = {}
    header_table = {}
    tree_root = FpTreeNode('root')
    # 第一次遍历数据库，寻找频繁1项集
    for item in data:
        for i in item:
            temp[i] = temp.get(i, 0) + data[item]
    for k in temp:
        if temp[k] >= support:
            header_table[k] = [temp[k], None]
    # 第二次遍历，构建FP树
    for item, count in data.items():
        item = order_item(item, header_table)
        insert_child(tree_root, item, header_table, count)
    return tree_root, header_table


# 数据格式转化
def data_process(data_set):
    result = {}
    for i in data_set:
        result[frozenset(i)] = 1
    return result


#生成前缀路径
def get_pre_path(node):
    result = []
    count = node.count
    while node.parent.name is not 'root':
        result.insert(0, node.parent.name)
        node = node.parent
    return {frozenset(result):count}


# 生成条件模式基
def cond_pat_base(start_node):
    result = {}
    node = start_node
    result.update(get_pre_path(node))
    while node.node_link is not None:
        node = node.node_link
        result.update(get_pre_path(node))
    return result


# 挖掘所有频繁模式
def fp_growth(data, support, level):
    tree, head = create_tree(data, support)
    tree.show()
    result = []
    if not len(head):
        return []
    for e in reversed(order_item(head.keys(), head)):
        #print(e,level)
        s = cond_pat_base(head[e][1])
        fp = fp_growth(s, support, level+1)
        if fp:
            for i in fp:
                i.append(e)
                result.append(i)
        result.append([e])
    #print(result)
    return result



if __name__ == '__main__':
    data = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    r = fp_growth(data_process(data), 3, 1)
    for i in r:print(i)

