from getopt import *
from time import *
from numpy import *
import sys
from random import *
import copy


# Read the network file
def network_reader(file_path):
    line_one = open(file_path).readline()
    ovr_data = str.split(line_one)
    vertex_num = int(ovr_data[0])
    edge_num = int(ovr_data[1])
    graph_edge = loadtxt(file_path, skiprows=1)
    # print(graph_edge)
    return vertex_num, edge_num, graph_edge


# Read the seed file
def seed_reader(file_path):
    seeds = set()
    lines = open(file_path).readlines()
    for line in lines:
        seeds.add(int(line.split()[0]))
    return seeds


class Graph:
    nodes = set()
    edges = []
    in_edges = []
    weight = {}

    def __init__(self, numpy_array, num_vertex):
        for i in range(0, num_vertex):
            self.add_node(i)
        for i in range(0, len(numpy_array)):
            self.add_edge(numpy_array[i][0], numpy_array[i][1], numpy_array[i][2])

    def add_node(self, value):
        self.nodes.add(value)
        self.edges.append([])
        self.in_edges.append([])

    def add_edge(self, from_node, to_node, weight):
        self.edges[int(from_node) - 1].append(int(to_node) - 1)
        self.in_edges[int(to_node) - 1].append(int(from_node) - 1)
        self.weight[(int(from_node) - 1, int(to_node) - 1)] = int(weight)

# def ic(target_graph, seed_set):
#     act_set = seed_set.copy()
#     all_set = seed_set.copy()
#     count = len(act_set)
#     while len(act_set) != 0:
#         new_act_set = set()
#         for item in act_set:
#             for neighbor in target_graph.edges[int(item) - 1]:
#                 if random() < target_graph.weight[(item - 1, neighbor)]:
#                     if neighbor + 1 not in all_set:
#                         new_act_set.add(neighbor + 1)
#                         all_set.add(neighbor + 1)
#         count = count + len(new_act_set)
#         act_set = new_act_set.copy()
#     return count
def ic(graph,seed):
    work=set(seed)
    all=set(seed)

    num=len(work)

    while work:
        new_work=set()
        for node in work:
            for near_node in graph.edges[node-1]:
                if random() < graph.weight[node-1,near_node]:
                    if near_node+1 not in all:
                        all.add(near_node+1)
                        new_work.add(near_node+1)
        num+=len(new_work)
        work=new_work
    return num

def it(graph,seed):
    work=seed.copy()
    all=seed.copy()
    num=0
    num+=len(work)
    ran={}
    for i in range(len(graph.nodes)):
        ran[i]=random()
        if ran[i] ==0 :
            work.add(i)
            all.add(i)
    while len(work)>0:
        new_work=set()
        for node in work:
            for near_node in graph.edges[node-1]:
                tol_weight = 0
                for n in graph.in_edges[near_node]:
                    if n + 1 in all:
                        tol_weight = tol_weight + graph.weight[(n, near_node)]
                if tol_weight > ran[near_node]:
                    if near_node + 1 not in all:
                        new_work.add(near_node + 1)
                        all.add(near_node + 1)
        num+=len(new_work)
        work=copy.deepcopy(new_work)
    return num


def greedy(graph, seed_num, model):
    num = 0
    ans = set()
    leng = len(graph.nodes)
    while num < seed_num:
        max_now = 0.0
        add_point = 0
        # print(num)
        for i in range(leng):
            if (i + 1) not in ans:
                ans.add(i + 1)
                sum = 0.0
                R = 100
                for j in range(0, R):
                    if model == "IC":
                        count = ic(graph, ans)
                    else:
                        count = it(graph, ans)
                    sum = count + sum
                if sum > max_now:
                    add_point = i + 1
                    max_now = sum
                ans.remove(i + 1)
        ans.add(add_point)
        num += 1
    return ans

def spread_check(graph, seed, model):
    global R
    sum = 0.0
    R=10000
    if model == "IC":
        for j in range(0, R):
            count = ic(graph, seed)
            sum = count + sum
    else:
        for j in range(0, R):
            count = it(graph, seed)
            sum = count + sum
    return sum / float(R)
def greedy_faster(graph, seed_num, model):
    ans=set()
    ans_list=dict()
    for i in range(len(graph.nodes)):
        ans_list[i+1]=spread_check(graph,{i+1},model)
    print("0")
    new_add=max(ans_list,key=ans_list.get)
    ans.add(new_add)
    ans_list.pop(new_add)
    while len(ans)<seed_num:
        new_add = max(ans_list, key=ans_list.get)
        ans_list[new_add]=spread_check(graph,ans|{new_add},model)
        new_add_2=max(ans_list, key=ans_list.get)
        if new_add==new_add_2:
            ans.add(new_add)
            ans_list.pop(new_add)
        else:
            continue
    return ans

def read_cmd():
    try:
        opts, agrs = getopt(sys.argv[0:], 'i:k:m:t')
    except:
        print("wrong in read cmd")
        sys.exit(2)
    graph_path = agrs[2]
    seed_num = int(agrs[4])
    model = agrs[6]
    time = int(agrs[8])
    return graph_path, seed_num, model, time


def main():
    # file_name=""
    # graph_path, seed_num, model, time=read_cmd()
    # begin=time()
    graph_path = 'network.txt'
    seed_num = 5
    model = 'IC'

    vertex_num, edge_num, graph_edge = network_reader(graph_path)
    # seed=seed_reader(seed_path)
    graph = Graph(graph_edge, vertex_num)
    # result = greedy(graph, 5, model)
    # {48, 53, 56, 58, 62}

    result = greedy_faster(graph, seed_num, model)
    # print(time()-begin)
    for p in result:
        print(p)

if __name__ == '__main__':
    main()
