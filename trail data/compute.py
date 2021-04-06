# -*- coding:utf-8 -*-
"""
@name:   compute.py
@time:   2020 / 04 / 07
@author: taifu
"""

import json
import os
import numpy as np


def solve1(resultFile, accuracy):
    methodName = resultFile['methodName']
    dataName = resultFile['dataName']
    time = min(resultFile['time'], 60)
    with open(ansPath + dataName + '.json', 'r') as fin:
        ansFile = json.loads(fin.read())
    aLabel = ansFile['labels']
    aLabelNum = set(aLabel)
    uLabel = resultFile['uLabelList']
    uLabelNum = set(uLabel)
    uLabelClu = {}
    uLabelNumReal = []
    F=[ 0 for i in range(len(aLabelNum))]
    C = [0 for i in range(len(aLabelNum))]
    for u in uLabelNum:
        if u != 0:
            uLabelClu[str(u)] = []
            uLabelNumReal.append(u)
    for i, u in enumerate(uLabel):
        if u != 0:
            uLabelClu[str(u)].append(aLabel[i])
    cl, clLabel, clLabelP = [], [], []
    for u in uLabelNumReal:
        ul = uLabelClu[str(u)]
        vl = []
        for v in aLabelNum:
            vl.append(ul.count(v))
        k = vl.index(max(vl))
        if(vl[k] >F[k]):
            F[k]=vl[k]
            C[k]=sum(vl)
    precision=sum(F)/sum(C)
    recall=sum(F)/len(aLabel)
    nu, na = len(uLabelNumReal), len(aLabelNum)
    accuracy[methodName][0].append(precision)
    accuracy[methodName][1].append(recall)
    accuracy[methodName][2].append(time)
    # exit()

def solve3(resultFile, accuracy):
    methodName = resultFile['methodName']
    dataName = resultFile['dataName']
    time = min(resultFile['time'], 30)
    with open(ansPath + dataName + '.json', 'r') as fin:
        ansFile = json.loads(fin.read())
    ans2 = ansFile['ans2'][1]
    aLabel = ansFile['labels']
    uLabel = resultFile['uLabelList']
    uLabelClu = []
    for i, u in enumerate(uLabel):
        if u != 0:
            uLabelClu.append(aLabel[i])
    nu = uLabelClu.count(ans2)
    p = nu / len(uLabelClu)
    r = nu / aLabel.count(ans2)
    accuracy[methodName][0].append(p)
    accuracy[methodName][1].append(r)
    accuracy[methodName][2].append(time)

def solve2(resultFile, accuracy):
    methodName = resultFile['methodName']
    dataName = resultFile['dataName']
    time = min(resultFile['time'], 30)
    with open(ansPath + dataName + '.json', 'r') as fin:
        ansFile = json.loads(fin.read())
    aLabel = ansFile['labels']
    ans3 = aLabel[ansFile['sp3']]
    uLabel = resultFile['uLabelList']
    uLabelClu = []
    for i, u in enumerate(uLabel):
        if u != 0:
            uLabelClu.append(aLabel[i])
    nu = uLabelClu.count(ans3)
    p = nu / len(uLabelClu)
    r = nu / aLabel.count(ans3)
    accuracy[methodName][0].append(p)
    accuracy[methodName][1].append(r)
    accuracy[methodName][2].append(time)

def solve4(resultFile, accuracy):
    methodName = resultFile['methodName']
    dataName = resultFile['dataName']
    time = min(resultFile['time'], 30)
    with open(ansPath + dataName + '.json', 'r') as fin:
        ansFile = json.loads(fin.read())
    aLabel = ansFile['labels']
    ans4 = ansFile['ans4'][0]
    uLabel = resultFile['uLabelList']
    uLabelClu = []
    for i, u in enumerate(uLabel):
        if u != 0:
            uLabelClu.append(aLabel[i])
    nu = uLabelClu.count(ans4)
    p = nu / len(uLabelClu)
    r = nu / aLabel.count(ans4)
    accuracy[methodName][0].append(p)
    accuracy[methodName][1].append(r)
    accuracy[methodName][2].append(time)

def solve5(resultFile, rank):
    mNameList = resultFile['methodNameList']
    uSortList = resultFile['uSortList']
    mList = resultFile['mList']
    for i, mName in enumerate(mNameList):
        pos = str(mList.index(i) + 1)
        mRank = uSortList.index(pos)
        rank[mName].append(12-mRank)

def task1(filePath):
    userList = os.listdir(filePath)
    print('task1')
    accuracyAll = {}
    accuracyAll['userList'] = userList
    accuracyAll['userNum'] = len(userList)
    accuracyAll['methodNameList'] = methodNameList
    for methodName in methodNameList:
        accuracyAll[methodName] = [[], [],[]]
    for user in userList:
        resultPath = filePath + user + '/'
        resultList = os.listdir(resultPath)
        accuracy = {}
        for methodName in methodNameList:
            accuracy[methodName] = [[], [],[]]
        for result in resultList:
            if result!='dmid1.json' and result!='dmid2.json' and result!='dmid3.json':
             with open(resultPath + result, 'r') as fin:
                resultFile = json.loads(fin.read())
                solve1(resultFile, accuracy)
        for methodName in methodNameList:
            accuracyAll[methodName][0].append(sum(accuracy[methodName][0]) / len(accuracy[methodName][0]))
            accuracyAll[methodName][1].append(sum(accuracy[methodName][1]) / len(accuracy[methodName][1]))
            accuracyAll[methodName][2].append(sum(accuracy[methodName][2]) / len(accuracy[methodName][2]))
    print(accuracyAll)
    savePath = './document/hypothesis/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    with open(savePath + 'task1.json', 'w') as fout:
        fout.write(json.dumps(accuracyAll))
    outp=[]
    outr=[]
    outt=[]
    for methodName in methodNameList:
        print(methodName, sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]),
              sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]))
        outr.append([round(sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]),4),methodName])
        outp.append([round(sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]),4), methodName])
        outt.append([round(sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]), 4), methodName])

    print('precision:',sorted(outp,reverse=True))
    print('recall:',sorted(outr,reverse=True))
    print('time:',sorted(outt))

def task2(filePath):
    userList = os.listdir(filePath)
    print('task2')
    accuracyAll = {}
    accuracyAll['userList'] = userList
    accuracyAll['userNum'] = len(userList)
    accuracyAll['methodNameList'] = methodNameList
    for methodName in methodNameList:
        accuracyAll[methodName] = [[], [], []]
    for user in userList:
        resultPath = filePath + user + '/'
        resultList = os.listdir(resultPath)
        accuracy = {}
        for methodName in methodNameList:
            accuracy[methodName] = [[], [], []]
        for result in resultList:
            if result != 'dmid1.json' and result != 'dmid2.json' and result != 'dmid3.json':
             with open(resultPath + result, 'r') as fin:
                resultFile = json.loads(fin.read())
                solve2(resultFile, accuracy)
        for methodName in methodNameList:
            p = sum(accuracy[methodName][0]) / len(accuracy[methodName][0])
            r = sum(accuracy[methodName][1]) / len(accuracy[methodName][1])
            t = sum(accuracy[methodName][2]) / len(accuracy[methodName][2])
            accuracyAll[methodName][0].append(p)
            accuracyAll[methodName][1].append(r)
            accuracyAll[methodName][2].append(t)
    savePath = './document/hypothesis/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    with open(savePath + 'task2.json', 'w') as fout:
        fout.write(json.dumps(accuracyAll))
    outp=[]
    outr=[]
    outt=[]
    for methodName in methodNameList:
        print(methodName, sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]),
              sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]),
              sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]))
        outr.append([sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]), methodName])
        outp.append([sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]), methodName])
        outt.append([sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]), methodName])

    print('precision:',sorted(outp,reverse=True))
    print('recall:',sorted(outr,reverse=True))
    print('time:',sorted(outt))

def task3(filePath):
    userList = os.listdir(filePath)
    print('task3')
    accuracyAll = {}
    accuracyAll['userList'] = userList
    accuracyAll['userNum'] = len(userList)
    accuracyAll['methodNameList'] = methodNameList
    for methodName in methodNameList:
        accuracyAll[methodName] = [[], [], []]
    for user in userList:
        resultPath = filePath + user + '/'
        resultList = os.listdir(resultPath)
        accuracy = {}
        for methodName in methodNameList:
            accuracy[methodName] = [[], [], []]
        for result in resultList:
            if result != 'dmid1.json' and result != 'dmid2.json' and result != 'dmid3.json':
             with open(resultPath + result, 'r') as fin:
                resultFile = json.loads(fin.read())
                solve3(resultFile, accuracy)
        for methodName in methodNameList:
            p = sum(accuracy[methodName][0]) / len(accuracy[methodName][0])
            r = sum(accuracy[methodName][1]) / len(accuracy[methodName][1])
            t = sum(accuracy[methodName][2]) / len(accuracy[methodName][2])
            accuracyAll[methodName][0].append(p)
            accuracyAll[methodName][1].append(r)
            accuracyAll[methodName][2].append(t)
    savePath = './document/hypothesis/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    with open(savePath + 'task2.json', 'w') as fout:
        fout.write(json.dumps(accuracyAll))
    outp=[]
    outr=[]
    outt=[]
    for methodName in methodNameList:
        print(methodName, sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]),
              sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]),
              sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]))
        outr.append([sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]), methodName])
        outp.append([sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]), methodName])
        outt.append([sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]), methodName])

    print('precision:',sorted(outp,reverse=True))
    print('recall:',sorted(outr,reverse=True))
    print('time:',sorted(outt))



def task4(filePath):
    userList = os.listdir(filePath)
    print('task4')
    accuracyAll = {}
    accuracyAll['userList'] = userList
    accuracyAll['userNum'] = len(userList)
    accuracyAll['methodNameList'] = methodNameList
    for methodName in methodNameList:
        accuracyAll[methodName] = [[], [], []]
    for user in userList:
        resultPath = filePath + user + '/'
        resultList = os.listdir(resultPath)
        accuracy = {}
        for methodName in methodNameList:
            accuracy[methodName] = [[], [], []]
        for result in resultList:
            if result != 'dmid1.json' and result != 'dmid2.json' and result != 'dmid3.json':
             with open(resultPath + result, 'r') as fin:
                resultFile = json.loads(fin.read())
                solve4(resultFile, accuracy)
        for methodName in methodNameList:
            p = sum(accuracy[methodName][0]) / len(accuracy[methodName][0])
            r = sum(accuracy[methodName][1]) / len(accuracy[methodName][1])
            t = sum(accuracy[methodName][2]) / len(accuracy[methodName][2])
            accuracyAll[methodName][0].append(p)
            accuracyAll[methodName][1].append(r)
            accuracyAll[methodName][2].append(t)

    savePath = './document/hypothesis/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    with open(savePath + 'task4.json', 'w') as fout:
        fout.write(json.dumps(accuracyAll))
    outp=[]
    outr=[]
    outt = []
    for methodName in methodNameList:
        print(methodName, sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]),
              sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]),
              sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]))
        outr.append([sum(accuracyAll[methodName][1]) / len(accuracyAll[methodName][1]), methodName])
        outp.append([sum(accuracyAll[methodName][0]) / len(accuracyAll[methodName][0]), methodName])
        outt.append([sum(accuracyAll[methodName][2]) / len(accuracyAll[methodName][2]), methodName])

    print('precision:',sorted(outp,reverse=True))
    print('recall:',sorted(outr,reverse=True))
    print('time:',sorted(outt))

def task5(filePath):
    userList = os.listdir(filePath)
    print('task5')
    rankAll = {}
    rankAll['userList'] = userList
    rankAll['userNum'] = len(userList)
    rankAll['methodNameList'] = methodNameList
    for methodName in methodNameList:
        rankAll[methodName] = []
    for user in userList:
        resultPath = filePath + user + '/'
        resultList = os.listdir(resultPath)
        rank = {}
        for methodName in methodNameList:
            rank[methodName] = []
        for result in resultList:
           if result != 'did0.json':
              with open(resultPath + result, 'r') as fin:
                resultFile = json.loads(fin.read())
                solve5(resultFile, rank)
        for methodName in methodNameList:
            rankAll[methodName].append(sum(rank[methodName]) / len(rank[methodName]))
    savePath = './document/hypothesis/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    with open(savePath + 'task5.json', 'w') as fout:
        fout.write(json.dumps(rankAll))
    for methodName in methodNameList:
        print(methodName, sum(rankAll[methodName]) / len(rankAll[methodName]))


if __name__ == '__main__':
    ansPath = './ground truth/'
    methodNameList = ['tsne', 'umap', 'isomap', 'mds', 'lle', 'le', 'lpp', 'npe', 'pca', 'fa', 'nmf', 'tsnle']
    dataNameList = ['boston', 'face5',  'olive', 'ecoli', 'mnist64', 'world12d'] # face5 is ExtYaleB
    task1('./formal study/E1/')
    task2('./formal study/E2/')
    task3('./formal study/E3/')
    task4('./formal study/E4/')
    task5('./formal study/E5/')
