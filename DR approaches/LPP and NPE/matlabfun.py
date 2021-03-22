import os
import numpy as np
import matlab.engine

def LPP(dataPath, filePath, k):
    eng1 = matlab.engine.start_matlab()
    result = eng1.runLPP(dataPath, k)
    np.savetxt(filePath + "lpp-" + str(k) + ".csv", result, delimiter=",")

def NPE(dataPath, filePath, k):
    eng2 = matlab.engine.start_matlab()
    result = eng2.runNPE(dataPath, k)
    np.savetxt(filePath + "npe-" + str(k) + ".csv", result, delimiter=",")

if __name__ == '__main__':
    k = 16
    dataRootPath = '../Data/'
    dataNameList = os.listdir(dataRootPath)
    for id, dataName in enumerate(dataNameList):
        dataPath = dataRootPath + dataName + '/' + dataName + '.csv'
        data = np.loadtxt(open(dataPath, "rb"), delimiter=",", skiprows=0)
        labelPath = dataRootPath + dataName + '/' + dataName + '-label.csv'
        label = np.loadtxt(open(labelPath, "rb"), delimiter=",", skiprows=0)
        print(id + 1, dataName, data.shape)
        filePath = dataRootPath + dataName + '/'
        LPP(dataPath, filePath, k)
        NPE(dataPath, filePath, k)


