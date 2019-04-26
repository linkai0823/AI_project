from numpy import *
import time
from getopt import *
import sys



#-------------------------------------------------------------------------------------------------------------------------------------------------
# pegasos method
def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split(' ')
        dataMat.append([float(lineArr[0]), float(lineArr[1]), float(lineArr[2]), float(lineArr[3]), float(lineArr[4]),float(lineArr[5]), float(lineArr[6]), float(lineArr[7]), float(lineArr[8]), float(lineArr[9])])
        labelMat.append(float(lineArr[10]))
    return dataMat, labelMat

def seqPegasos(dataSet, labels, lam, T,time_limit,star_time):
    m, n = shape(dataSet)
    w = zeros(n)
    for t in range(1, T + 1):
        if  time.time()-star_time>time_limit-1:
            break
        i = random.randint(m)
        eta = 1.0 / (lam * t)
        p = w*(dataSet[i, :].T)
        if labels[i] * p < 1:
            w = (1.0 - 1 / t) * w + eta * labels[i] * dataSet[i, :]
        else:
            w = (1.0 - 1 / t) * w
        #print w
    return w




#pegasos method over------------------------------------------------------------------------------------------------------------------------------------

#
# #smop method-----------------------------------------------------------------------------------------------------------------------------------------------
# #take all data in class
# class Smo_data:
#     def __init__(self, dataMatIn, classLabels, C, toler):  # Initialize the structure with the parameters
#         self.X = dataMatIn
#         self.labelMat = classLabels
#         self.C = C
#         self.tol = toler
#         self.m = shape(dataMatIn)[0]
#         self.alphas = mat(zeros((self.m, 1)))
#         self.b = 0
#         self.eCache = mat(zeros((self.m, 2)))
#
# #main
# def smoP(dataMatIn, classLabels, C, toler, maxIter):
#     oS = optStruct(mat(dataMatIn), mat(classLabels).transpose(), C, toler)
#     iter = 0
#     entireSet = True
#     alphaPairsChanged = 0
#     while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
#         alphaPairsChanged = 0
#         if entireSet:
#             for i in range(oS.m):
#                 alphaPairsChanged += innerL(i, oS)
#             iter += 1
#         else:
#             nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
#             for i in nonBoundIs:
#                 alphaPairsChanged += innerL(i, oS)
#             iter += 1
#         if entireSet:
#             entireSet = False
#         elif (alphaPairsChanged == 0):
#             entireSet = True
#     return oS.b, oS.alphas

def read_cmd():
    try:
        opts, agrs = getopt(sys.argv[0:], ' : :t')
    except:
        print("wrong in read cmd")
        sys.exit(2)
    # print(agrs)
    train = agrs[1]
    test = agrs[2]
    time_limit = float(agrs[4])
    return train, test, time_limit

def loadTraindata(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split(' ')
        dataMat.append([float(lineArr[0]), float(lineArr[1]), float(lineArr[2]), float(lineArr[3]), float(lineArr[4]),
                        float(lineArr[5]), float(lineArr[6]), float(lineArr[7]), float(lineArr[8]), float(lineArr[9])])
    return dataMat

def main():
    train,test,time_limit=read_cmd()
    # print(train,test,time_limit)

    # train="train_data.txt"
    # test="o.txt"
    # time_limit=10
    star_time=time.time()
    datArr, labelList = loadDataSet(train)
    datMat = mat(datArr)
    finalWs = seqPegasos(datMat, labelList, 2, 1000,time_limit,star_time)
    # python SVM.py train_data.txt o.txt -t 11

    # te,tes=loadDataSet(test)
    dataMat1 = loadTraindata(test)
    test_len=shape(dataMat1)
    re=0
    # print(time.time()-star_time)
    for i in range(test_len[0]):
        res=sum(multiply(finalWs,dataMat1[i]))
        if res>0:
            print(1)
        else:
            print(-1)
        re+=1

    print(re)




if __name__ == '__main__':
        main()
