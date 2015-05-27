import buildwd
import numpy as np
from sklearn import linear_model
from sklearn import neighbors

def tfidf(mat=None, rownames=None):
    """TF-IDF on mat. rownames is unused; it's an argument only 
    for consistency with other methods used here"""
    colsums = np.sum(mat, axis=0)
    doccount = mat.shape[1]
    w = np.array([_tfidf_row_func(row, colsums, doccount) for row in mat])
    return (w, rownames)

def _tfidf_row_func(row, colsums, doccount):
    df = float(len([x for x in row if x > 0]))
    idf = 0.0
    # This ensures a defined IDF value >= 0.0:
    if df > 0.0 and df != doccount:
        idf = np.log(doccount / df)
    tfs = row/colsums
    return tfs * idf

def tfidf_logreg(train_file):
    wd = buildwd.buildWD(train_file)
    colnames = wd[1]
    rownames = wd[2]
    subjects = wd[3]
    idf = tfidf(wd[0], rownames)
    
    trainMat = np.zeros((len(colnames), wd[0].shape[1]))
    f = open(train_file)
    matCol = 0
    for line in f:
        words = line.split()
        if words[0] in colnames:
            trainRow = np.zeros(wd[0].shape[1])
            numWords = 0
            for word in words[2:]:
                pword = buildwd.processWord(word)
                if pword in rownames:
                    numWords += 1
                    trainRow = trainRow + idf[0][rownames.index(pword)]
            trainRow = (trainRow*1.0) / numWords
            trainMat[matCol,:] = trainRow
            matCol += 1
    f.close()

    trainVals = np.zeros(len(subjects))
    for s in enumerate(subjects):
        if s[1] == 'Sports':
            trainVals[s[0]] = 1
            
    logreg = linear_model.LogisticRegression()
    logreg.fit(trainMat[0:(trainMat.shape[0]*0.7),:], trainVals[0:(trainMat.shape[0]*0.7)])
    return logreg.score(trainMat[(trainMat.shape[0]*0.7):,:], trainVals[(trainMat.shape[0]*0.7):])

def tfidf_knn(train_file):
    wd = buildwd.buildWD(train_file)
    colnames = wd[1]
    rownames = wd[2]
    subjects = wd[3]
    idf = tfidf(wd[0], rownames)
    
    trainMat = np.zeros((len(colnames), wd[0].shape[1]))
    f = open(train_file)
    matCol = 0
    for line in f:
        words = line.split()
        if words[0] in colnames:
            trainRow = np.zeros(wd[0].shape[1])
            numWords = 0
            for word in words[2:]:
                pword = buildwd.processWord(word)
                if pword in rownames:
                    numWords += 1
                    trainRow = trainRow + idf[0][rownames.index(pword)]
            trainRow = (trainRow*1.0) / numWords
            trainMat[matCol,:] = trainRow
            matCol += 1
    f.close()

    trainVals = np.zeros(len(subjects))
    for s in enumerate(subjects):
        if s[1] == 'Sports':
            trainVals[s[0]] = 1
            
    knn = neighbors.KNeighborsClassifier()
    knn.fit(trainMat[0:(trainMat.shape[0]*0.7),:], trainVals[0:(trainMat.shape[0]*0.7)])
    return knn.score(trainMat[(trainMat.shape[0]*0.7):,:], trainVals[(trainMat.shape[0]*0.7):])

score = tfidf_knn("training.txt")

            

