from getopt import *
from time import *
import numpy as ns
import sys
from random import *
import multiprocessing
import math

import copy as cp
start = 0
ran_seed = 0
vertices = 0
depot = -1
capacity = -1
graph_data = []
threads = []


def get_input(file_name):
    # file_name = 'val7A.dat'

    file = open(file_name)
    file.readline()

    global vertices
    new_line = file.readline()
    get_value = (new_line).split(':')
    vertices = int(get_value[1])

    global depot
    new_line = file.readline()
    get_value = new_line.split(':')
    depot = int(get_value[1])

    new_line = file.readline()
    get_value = new_line.split(':')
    sum_a = int(get_value[1])

    new_line = file.readline()
    get_value = new_line.split(':')
    sum_b = int(get_value[1])

    global sum_num
    sum_num = sum_a + sum_b

    file.readline()
    global capacity
    new_line = file.readline()
    get_value = new_line.split(':')
    capacity = int(get_value[1])

    global total_work
    new_line = file.readline()
    get_value = new_line.split(':')
    total_work = int(get_value[1])

    file_new = open(file_name).readlines()
    file_new = file_new[:-1]
    global graph_data
    graph_data = ns.loadtxt(file_new, skiprows=9)
    # global ter_time
    # for name, value in options:
    #     if name in "-t":
    #         ter_time = int(value)
    #     if name in "-s":
    #         ran_seed = int(value)






def dijsktra(graph_get, point):
    visited = {point: 0}
    nodes = set(graph_get.nodes)
    while nodes:
        min_node = -1
        for node in nodes:
            if node in visited:
                if min_node == -1:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node == -1:
            break
        nodes.remove(min_node)
        current_weight = visited[min_node]
        for i in range(1,vertices+1):
            if graph_get.graph_cost[min_node][i]>0:
                weight = current_weight + graph_get.graph_cost[min_node][i]
                if i not in visited or weight < visited[i]:
                    visited[i] = weight
    return visited


def all_dij(graph_get, vertices):
    min_cost = ns.zeros((vertices+1, vertices+1))
    for i in range(1, vertices+1):
        visited = dijsktra(graph_get, i)

        for j in range(1, vertices+1):
            if j != i:
                min_cost[i][j] = visited.get(j)
                min_cost[j][i] = visited.get(j)

    return min_cost


def go_one_car(graph_get, min_cost,need_work,work_dic):  #min_cost dijis 结果 need_work 剩余工作量
    cap = capacity
    list_choice=[]
    find=0
    end_choice=[]
    cost=0
    first=depot
    return_str=''
    car_path=[]
    while cap>0 and need_work >0:
        find = 0
        list_choice.clear()
        for key in work_dic:
            if work_dic[key]<=cap:
                list_choice.append(key[0])
                list_choice.append(key[1])
        min_dis=99999
        point=0

        for i in range(int(len(list_choice)/2)):
            dis_i=min(min_cost[first][list_choice[point]],min_cost[first][list_choice[point+1]])
            if dis_i<min_dis:
                find=1
                min_dis=dis_i
                end_choice.clear()
                end_choice.append(list_choice[point])
                end_choice.append(list_choice[point+1])
            if dis_i==min_dis:
                end_choice.append(list_choice[point])
                end_choice.append(list_choice[point + 1])
            point+=2
        if find==0:
            break
        if len(end_choice) ==2 :
            cost+=min_dis
            flag=False
            cost+=graph_get.graph_cost[end_choice[0]][end_choice[1]]
            cap-=graph_get.graph_work[end_choice[0]][end_choice[1]]
            work_dic[(min((end_choice[0], end_choice[1])), max(end_choice[0], end_choice[1]))] = 9999999
            need_work-=graph_get.graph_cost[end_choice[0]][end_choice[1]]


            if min_dis==min_cost[first][end_choice[0]]:
                # if first!=end_choice[0]:
                #
                #     return_str += str((first, end_choice[0]))
                #     return_str += ","
                return_str += str((end_choice[0], end_choice[1]))
                car_path.append(end_choice[0])
                car_path.append(end_choice[1])

                return_str += ','
                first=end_choice[1]
                flag=True
            if min_dis == min_cost[first][end_choice[1]] and flag==False:
                # if first!=end_choice[1]:
                #
                #     return_str += str((first, end_choice[1]))
                #     return_str += ","
                first = end_choice[0]
                car_path.append(end_choice[1])
                car_path.append(end_choice[0])
                car_path.append((end_choice[1], end_choice[0]))

                return_str += ','
        if len(end_choice) > 2 :#多种策略选择 random 拯救世界
            cost += min_dis
            flag = False
            fi=randint(1,int(len(end_choice)/2))
            cost += graph_get.graph_cost[end_choice[2*fi-2]][end_choice[2*fi-1]]
            cap -= graph_get.graph_work[end_choice[2*fi-2]][end_choice[2*fi-1]]
            work_dic[(min((end_choice[2*fi-2], end_choice[2*fi-1])), max(end_choice[2*fi-2], end_choice[2*fi-1]))] = 9999999
            need_work -= graph_get.graph_cost[end_choice[2*fi-2]][end_choice[2*fi-1]]


            if min_dis == min_cost[first][end_choice[2*fi-2]]:
                # if first!=end_choice[0]:
                #     return_str += str((first, end_choice[0]))
                #     return_str += ","
                first = end_choice[2*fi-1]

                return_str += str((end_choice[2*fi-2], end_choice[2*fi-1]))
                car_path.append(end_choice[2*fi-2])
                car_path.append(end_choice[2*fi-1])

                return_str += ','
                flag = True
            if min_dis == min_cost[first][end_choice[2*fi-1]] and flag == False:
                # if first!=end_choice[1]:
                #
                #     return_str += str((first, end_choice[1]))
                #     return_str += ","
                first = end_choice[2*fi-2]
                return_str += str((end_choice[2*fi-1], end_choice[2*fi-2]))
                car_path.append(end_choice[2*fi-1])
                car_path.append(end_choice[2*fi-2])

                return_str += ','
        if len(end_choice) == 0:
            break
    cost+=min_cost[depot][first]
    return cost,need_work,return_str,car_path

def get_parameter():
    result=[]
    _,args=getopt(sys.argv[0:2],"")
    opts,_=getopt(sys.argv[2:],"t:s:")
    result.append(args[1])
    for i in opts:
        result.append(i[1])
    return result

def main():
    file_name = 'egl-s1-A.dat'
    # res=get_parameter()
    # file_name = res[0]
    # time_limit = int(res[1])
    # seed = int(res[2])
    end_cos=99999999999
    end_str=''
    end_path=[]
    get_input(file_name)
    graph_get = Graph(graph_data)

    min_cost=all_dij(graph_get,vertices)
    graph_get=Graph(graph_data)

    for r in range(10000):
        print(r)
        need=total_work
        cos=0
        path=[]
        add_str=""
        work_dic=cp.deepcopy(graph_get.work_dict)
        while need>0:
            add_str += '0'
            add_str += ','
            a,b,c,d=go_one_car(graph_get,min_cost,need,work_dic)
            add_str+=c
            need=b
            path.append(d)
            if need>0:
                add_str+='0'
                add_str+=','
            else:
                add_str+='0'
            cos+=a
        cos=int(cos)
        if cos<end_cos:
            # print(r,cos)
            end_cos=cos
            end_str=add_str
            end_path=path


    x=''
    y=''
    end=end_cos
    do_flag=0
         # print(end_path)
    x,y=go_mountain_burn(graph_get,end_path,min_cost,end)
    # print('s' + ' ' + end_str)
    # print('q' + ' ' + str(end_cos))
    # print(end_path[0])
    # aaa=swap_two_point(end_path,0,1,0,2)
    # print(end_path[0])
    print('s' + ' ' + path_to_answer(end_path))
    print('q' + ' ' + str(end_cos))

    print('s' + ' ' + path_to_answer(y))
    print('q' + ' ' + str(x))

def path_to_answer(path):
    str_an=''
    for i in range(len(path)):
        str_an+='0,'
        for j in range(int(len(path[i])/2)):

            str_an+='('
            str_an+=str(path[i][j*2])
            str_an+=','
            str_an+=str(path[i][j*2+1])
            str_an+='),'

        if i==(len(path)-1):
            str_an+='0'
        else:
            str_an+='0,'
    return str_an

def cal_path_cost(path,min_cost,graph_get):
    sum_cost=0
    for i in range(len(path)):
        fr = depot
        point=0
        while point <(len(path[i])):
            to=path[i][point]
            sum_cost+=min_cost[fr][to]
            fr=to
            to=path[i][point+1]
            sum_cost+=graph_get.graph_cost[fr][to]
            fr=to
            point+=2
        sum_cost+=min_cost[fr][depot]
    return  sum_cost
def swap_one_point(path_get,i,j):
    path=cp.deepcopy(path_get)
    temp=path[i][j*2]
    path[i][j*2]=path[i][j*2+1]
    path[i][j*2+1]=temp
    return path
def swap_two_point(path_get,i,j,i1,j1):
    path=cp.deepcopy(path_get)
    x = path[i][j * 2]
    y = path[i][j * 2 + 1]
    path[i].pop(j*2)
    path[i].pop(j*2)
    path[i1].insert(j1*2,x)
    path[i1].insert(j1*2+1,y)

    return path
def cal_cap(path,graph_get):
    path_cap=0
    point = 0
    while point < (len(path)):
        path_cap+=graph_get.graph_work[path[point]][path[point+1]]
        point+=2
    if path_cap>capacity:
        return False
    else:
        return True

def go_mountain(graph_get,path,min_cost,old_cost):
    end_cost=old_cost
    lenth=len(path)
    end_path=cp.copy(path)
    for i in range(lenth):
        for j in range(int(len(path[i])/2)):
            new_path=swap_one_point(path,i,j)
            cost=cal_path_cost(new_path,min_cost,graph_get)
            if cost<=end_cost:
                end_cost=cost
                end_path=new_path

    for i in range(lenth):
        for j in range(int(len(path[i])/2)):
            point=i
            point_2=j
            for o in range(point+1,lenth):
                for q in range(point_2,int(len(path[o])/2)):
                    new_path = swap_two_point(path,i,j,o,q)
                    if cal_cap(new_path[i],graph_get)and cal_cap(new_path[o],graph_get):
                        cost = cal_path_cost(new_path, min_cost, graph_get)
                        if cost <= end_cost:
                            end_cost = cost
                            end_path = new_path
    return end_cost,end_path

def go_mountain_burn(graph_get,path,min_cost,old_cost):
    end_cost=old_cost
    lenth=len(path)
    end_path=cp.copy(path)
    best_path=cp.copy(path)
    best_cost=old_cost
    T=old_cost*old_cost/0.85
    ti=time()
    while T >old_cost*1:
        T*=0.85
        for z in range(4):
            for i in range(lenth):
                for j in range(int(len(end_path[i])/2)):
                    new_path=swap_one_point(end_path,i,j)
                    cost=cal_path_cost(new_path,min_cost,graph_get)
                    der=cost-old_cost
                    if cost<old_cost:
                        end_cost=cost
                        end_path=new_path
                        best_cost=cost
                        best_path=new_path
                    flag=random()
                    if der>=0:
                        if flag<math.exp(-der/T):
                                end_cost=cost
                                end_path=new_path


            for i in range(lenth):
                end=int(len(end_path[i])/2)
                j=0
                while j <end :
                    end = int(len(end_path[i]) / 2)
                    for q in range(j + 1, end):
                        if (int(len(end_path[i]) / 2)-1)<j*2:
                            break
                        new_path = swap_two_point(end_path, i, j, i, q)
                        if cal_cap(new_path[i], graph_get) and cal_cap(new_path[i], graph_get):
                            cost = cal_path_cost(new_path, min_cost, graph_get)
                            der = cost - old_cost
                            if cost < old_cost:
                                best_cost = cost
                                best_path = new_path
                                end_cost = cost
                                end_path = new_path
                            flag = random()
                            if der >= 0:
                                if flag < math.exp(-der / T):
                                    end_cost = cost
                                    end_path = new_path
                    for o in range(i+1,lenth):
                        for q in range(int(len(end_path[o])/2)):

                            new_path = swap_two_point(end_path,i,j,o,q)
                            if cal_cap(new_path[i],graph_get)and cal_cap(new_path[o],graph_get):
                                cost = cal_path_cost(new_path, min_cost, graph_get)
                                der = cost - old_cost
                                if cost < old_cost:
                                    best_cost = cost
                                    best_path = new_path
                                    end_cost = cost
                                    end_path = new_path
                                flag = random()
                                if der >= 0:
                                    if flag < math.exp(-der / T):
                                        end_cost = cost
                                        end_path = new_path
                    j+=1
        new_ti=time()
        if ti-new_ti>20:
            break
    return best_cost,best_path

class Graph:
    nodes = set()
    edges = []
    distances = {}
    work_dict = {}
    graph_cost=ns.zeros(1)
    graph_work=ns.zeros(1)

    def __init__(self,graph_data):
        self.graph_cost = ns.zeros((len(graph_data), len(graph_data)))
        self.graph_work = ns.zeros((len(graph_data), len(graph_data)))

        for i in range(0, sum_num):
            x = int(graph_data[i][0])
            y = int(graph_data[i][1])
            cost = int(graph_data[i][2])
            work = int(graph_data[i][3])
            self.graph_cost[x][y] = cost
            self.graph_cost[y][x] = cost
            self.graph_work[x][y] = work
            self.graph_work[y][x] = work
            if work>0:
                self.work_dict[(min((int(x), int(y))), max((int(x), int(y) )))] = work
        for i in range(1, vertices+1):
            self.add_node(i)
        for i in range(0, sum_num):
            self.edges.append([])
            self.edges.append([])
        for i in range(0, sum_num):
            self.add_edge(graph_data[i][0], graph_data[i][1], graph_data[i][2])

    def add_node(self, value):
        self.nodes.add(value)


    def add_edge(self, from_node, to_node, distance):

        self.edges[int(from_node) - 1].append(int(to_node) - 1)
        self.edges[int(to_node) - 1].append(int(from_node) - 1)
        self.distances[((int(from_node) - 1, int(to_node) - 1))] = int(distance)
        self.distances[((int(to_node) - 1, int(from_node) - 1))] = int(distance)
if __name__ == '__main__':
    main()
    exit(0)
