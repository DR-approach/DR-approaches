# -*- coding:utf-8 -*-

import os
from sklearn.decomposition import PCA, FactorAnalysis, NMF
from sklearn.manifold import TSNE, Isomap, MDS, LocallyLinearEmbedding, SpectralEmbedding
from sklearn.manifold import TSNLE        # You need to copy t_snle.py to the directory where t_SNE.py is located
from sklearn import preprocessing
import numpy as np
import umap
import matlab.engine

def getLe(data, k):
    le = SpectralEmbedding(n_components=2, n_neighbors=k)
    result = le.fit_transform(data)
    return result

def getLle(data, k):
    LLE = LocallyLinearEmbedding(n_neighbors=k, n_components=2, max_iter=200)
    result = LLE.fit_transform(data)
    return result

def getIsomap(data, k):
    isomap = Isomap(n_neighbors=k, n_components=2)
    result = isomap.fit_transform(data)
    return result

def getMds(data):
    mds = MDS(n_components=2, max_iter=500)
    result = mds.fit_transform(data)
    return result

def getTsne(data, k):
    tsne = TSNE(method='exact',n_components=2, perplexity=k, early_exaggeration=6, n_iter=3000)
    result = tsne.fit_transform(data)
    return result

def getTsnle(data, k):
    tsnle = TSNLE(method='exact',n_components=2, perplexity=k, early_exaggeration=6, n_iter=3000)
    result = tsnle.fit_transform(data)
    return result

def getPca(data):
    pca = PCA(n_components=2)
    result = pca.fit_transform(data)
    return result

def getFA(data):
    fa = FactorAnalysis(n_components=2, max_iter=2000)
    result = fa.fit_transform(data)
    return result

def getNMF(data):
    nmf = NMF(n_components=2, max_iter=400)
    result = nmf.fit_transform(data)
    return result

def getUmap(data, k):
    result = umap.UMAP(n_neighbors=k,n_epochs=500).fit_transform(data)
    return result

def getLPP(dataPath, k):
    eng1 = matlab.engine.start_matlab()
    result = eng1.runLPP(dataPath, k)
    return result


def getNPE(dataPath, k):
    eng2 = matlab.engine.start_matlab()
    result = eng2.runNPE(dataPath, k)
    return result


if __name__ == '__main__':
    dataRootPath = '../Data/'
    dataNameList = os.listdir(dataRootPath)
    k = 10
    for dataName in dataNameList:
        print(dataName)
        dataPath = dataRootPath + dataName + '/' + dataName + '.csv'
        labelPath = dataRootPath + dataName + '/' + dataName + '-label.csv'
        data = np.loadtxt(open(dataPath, "rb"), delimiter=",", skiprows=0)
        label = np.loadtxt(open(labelPath, "rb"), delimiter=",", skiprows=0)
        data = preprocessing.MinMaxScaler().fit_transform(data)
        tsneResult = getTsne(data, k)
        leResult = getLe(data, k)
        isomapResult = getIsomap(data, k)
        mdsResult = getMds(data)
        tsnleResult = getTsnle(data, k)
        pcaResult = getPca(data)
        lleResult = getLle(data, k)
        faResult = getFA(data)
        nmfResult = getNMF(data)
        umapResult = getUmap(data, k)
        lppResult=getLPP(dataPath, k)
        npeResult=getNPE(dataPath,float(k)) #Integer of type float

        filePath = dataRootPath + dataName + '/'
        np.savetxt(filePath + "tsne.csv", tsneResult, delimiter=",")
        np.savetxt(filePath + "le.csv", leResult, delimiter=",")
        np.savetxt(filePath + "isomap.csv", isomapResult, delimiter=",")
        np.savetxt(filePath + "mds.csv", mdsResult, delimiter=",")
        np.savetxt(filePath + "tsnle.csv", tsnleResult, delimiter=",")
        np.savetxt(filePath + "pca.csv", pcaResult, delimiter=",")
        np.savetxt(filePath + "lle.csv", lleResult, delimiter=",")
        np.savetxt(filePath + "fa.csv", faResult, delimiter=",")
        np.savetxt(filePath + "nmf.csv", nmfResult, delimiter=",")
        np.savetxt(filePath + "umap.csv", umapResult, delimiter=",")
        np.savetxt(filePath + "lpp.csv", lppResult, delimiter=",")
        np.savetxt(filePath + "npe.csv", npeResult, delimiter=",")
