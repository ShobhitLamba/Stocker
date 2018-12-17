# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 22:48:08 2018

@author: Sakshi Panday

@Overview
"""
#from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE

# =============================================================================
# SMOTE for creating synthetic observations of the minority class
# =============================================================================
def oversample(trainX, trainY):
    sm = SMOTE(ratio = 1.0)
    return sm.fit_sample(trainX, trainY)

# =============================================================================
# view the decision tree created
# =============================================================================
def showTree(model):
    from sklearn.externals.six import StringIO  
    from IPython.display import Image  
    from sklearn.tree import export_graphviz
    import pydotplus
    dot_data = StringIO()
    export_graphviz(model, out_file=dot_data,  
                    filled=True, rounded=True,
                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
    Image(graph.create_png())
    
def preprocessing(df, colList):
    from sklearn.preprocessing import LabelEncoder, MinMaxScaler
    df = df.apply(LabelEncoder().fit_transform)
    df = pd.DataFrame(MinMaxScaler().fit_transform(df.values), columns = df.columns)    
    
def predict(df, colList):
    
    techAnalysis = {}
    techAnalysis['Models'] = np.array(['Low','High','Prediction'])
    
    '''data prep'''
    preprocessing(df, colList)
    
    '''Train and Test split'''
    split = int(len(df)*0.0060)
#    print(split)
#    split = 4481
#    train = df[:split]
    train = df[split:]
    test = df[split:]
    print(len(train))
    train = train[-60:]
    test = test[:30]
    
    '''Training and Testing Models:
        Logistic Reg
        Decision Tree
        SVC
        KNN
        MLP
        RandomForest
        Ensemble'''
        
    from sklearn.linear_model import LogisticRegression
    Xtrain = train[colList]
    ytrain = train['realHL']
#    Xtrain, ytrain = oversample(Xtrain,ytrain)
    Xtest = test[colList]
    ytest = test['realHL']
    print(ytest)
    from sklearn.metrics import precision_recall_fscore_support
    from sklearn.metrics import classification_report
    target_names = ['False', 'True']
    
    #LogReg
    print('_____________')
    clflr = LogisticRegression(random_state=0, solver='lbfgs',
                             multi_class='multinomial').fit(Xtrain, ytrain)
    print('LogReg:', clflr.score(Xtest, ytest), clflr.predict(Xtest),classification_report(ytest, clflr.predict(Xtest), target_names=target_names)) #, average='binary'
    clf_rep = precision_recall_fscore_support(ytest, clflr.predict(Xtest))   
    techAnalysis['Logistic Regression'] = clf_rep[2].round(2)
    
    #decision tree
    print('_____________')
    from sklearn import tree
    from sklearn.tree import DecisionTreeClassifier
    clfdt = DecisionTreeClassifier().fit(Xtrain, ytrain)    #max_depth = 2
    print('DTtrain:',clfdt.score(Xtest, ytest))
    print(clfdt.predict(Xtest))
    print(classification_report(ytest,
          clfdt.predict(Xtest), target_names=target_names),'\n\n') 
    clf_rep = precision_recall_fscore_support(ytest, clfdt.predict(Xtest))   
    techAnalysis['Decision Tree'] = clf_rep[2].round(2)
#    tree.export_graphviz(clf,out_file='tree.dot')

    #SVM
    print('_____________')
    from sklearn.svm import SVC
    clfsvc = SVC(gamma='auto')
    clfsvc.fit(Xtrain, ytrain)
    print(clfsvc.predict(Xtest))
    print('SVC:', clfsvc.score(Xtest, ytest),classification_report(ytest, clfsvc.predict(Xtest), target_names=target_names),'\n')
    clf_rep = precision_recall_fscore_support(ytest, clfsvc.predict(Xtest))   
    techAnalysis['Support Vector Machine'] = clf_rep[2].round(2)

    #K-Nearest Neighbors
    print('_____________')
    from sklearn.neighbors import KNeighborsClassifier
    clfknn = KNeighborsClassifier(2)
    clfknn.fit(Xtrain, ytrain)
    print(clfknn.predict(Xtest))
    print('KNN:', clfknn.score(Xtest, ytest),classification_report(ytest, clfknn.predict(Xtest), target_names=target_names))
    clf_rep = precision_recall_fscore_support(ytest, clfknn.predict(Xtest))   
    techAnalysis['K-Nearest Neighbors'] = clf_rep[2].round(2)
    
    
    #Multi-layer Perceptron
    print('_____________')
    from sklearn.neural_network import MLPClassifier
    clfmlp = MLPClassifier(alpha=1)
    clfmlp.fit(Xtrain, ytrain)
    print(clfmlp.predict(Xtest))
    print('MLP:', clfmlp.score(Xtest, ytest),classification_report(ytest, clfmlp.predict(Xtest), target_names=target_names))
    clf_rep = precision_recall_fscore_support(ytest, clfmlp.predict(Xtest))   
    techAnalysis['Multi-layer Perceptron'] = clf_rep[2].round(2)    
    
    from sklearn.ensemble import RandomForestClassifier, VotingClassifier
    #Random Forest Trees
    print('_____________')
    clfrft = RandomForestClassifier()
    clfrft.fit(Xtrain, ytrain)
    print(clfrft.predict(Xtest))
    print('Random Forest:', clfrft.score(Xtest, ytest),classification_report(ytest, clfrft.predict(Xtest), target_names=target_names))
    clf_rep = precision_recall_fscore_support(ytest, clfrft.predict(Xtest))   
    techAnalysis['Random Forest'] = clf_rep[2].round(2)        
    
    #voting classifier
    print('_____________')
    eclf3 = VotingClassifier(estimators=[
       ('lr', clflr), ('dt', clfdt), ('svc', clfsvc), ('knn', clfknn), ('mlp', clfmlp), ('rft',clfrft)],
       voting='hard', 
       flatten_transform=True) #weights=[1,1,1],
    eclf3 = eclf3.fit(Xtrain, ytrain)
    print(eclf3.predict(Xtest))
    print('Ensemble:', eclf3.score(Xtest, ytest),
          classification_report(ytest, eclf3.predict(Xtest),
                                target_names=target_names),'\n')

    clf_rep = precision_recall_fscore_support(ytest, eclf3.predict(Xtest))   
    techAnalysis['Intelligent Average'] = clf_rep[2].round(2)
    
#    dataframe = pd.DataFrame.from_dict(techAnalysis)
#    dataframe.to_csv('Technical_Analysis_Report.csv', index = False)
    
    '''
    For single indicator
    '''

#    #LogReg
#    clflr = LogisticRegression(random_state=0, solver='lbfgs',
#                             multi_class='multinomial').fit(np.array(Xtrain).reshape(-1,1), ytrain)
#    print('LogReg:',clflr.score(np.array(Xtest).reshape(-1,1), ytest),clflr.predict(np.array(Xtest).reshape(-1,1)).reshape(-1,1),classification_report(ytest, clflr.predict(np.array(Xtest).reshape(-1,1)), target_names=target_names)) #, average='binary'
#    print('______')
#    #decision tree
#    from sklearn import tree
#    from sklearn.tree import DecisionTreeClassifier
#    clf = DecisionTreeClassifier(max_depth = 10).fit(np.array(Xtrain).reshape(-1,1), ytrain)    
#    print('DTtrain:',clf.score(np.array(Xtest).reshape(-1,1), ytest))
#    print(classification_report(ytest,
#          clf.predict(np.array(Xtest).reshape(-1,1)), target_names=target_names),'\n\n')
#    print(clf.predict(np.array(Xtest).reshape(-1,1)))
#    print('______')
##    tree.export_graphviz(clf,out_file='tree.dot')
##
##
##    
#    #SVM
#    from sklearn.svm import SVC
#    clf = SVC(gamma='auto')
#    clf.fit(np.array(Xtrain).reshape(-1,1), ytrain)
#    print('SVC:',clf.score(np.array(Xtest).reshape(-1,1), ytest),classification_report(ytest, clf.predict(np.array(Xtest).reshape(-1,1)), target_names=target_names),'\n',clf.predict(np.array(Xtest).reshape(-1,1)))
#    print(clf.predict(np.array(Xtest).reshape(-1,1)))
#    print('______')
#    #randomforest
#    from sklearn.neighbors import KNeighborsClassifier
#    clf = KNeighborsClassifier(2)
#    clf.fit(np.array(Xtrain).reshape(-1,1), ytrain)
#    print('KNN:',clf.score(np.array(Xtest).reshape(-1,1), ytest),classification_report(ytest, clf.predict(np.array(Xtest).reshape(-1,1)), target_names=target_names))
#    print(clf.predict(np.array(Xtest).reshape(-1,1)))