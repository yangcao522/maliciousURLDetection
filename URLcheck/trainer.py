#!/usr/bin/python
# -*- coding:utf8 -*-

import pandas
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import numpy
from sklearn import svm
# from sklearn import cross_validation as cv
from sklearn.model_selection import cross_val_score
import matplotlib.pylab as plt
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas", lineno=570)


def return_nonstring_col(data_cols):
    cols_to_keep = []
    train_cols = []
    for col in data_cols:
        if col != 'URL' and col != 'host' and col != 'path':
            cols_to_keep.append(col)
            if col != 'malicious' and col != 'result':
                train_cols.append(col)
    return [cols_to_keep, train_cols]


def svm_classifier(train, query, train_cols):
    #Support Vector Classification(支持向量机分类，应该就是SVM的分类模型)
    clf = svm.SVC()

    #训练集数据
    train[train_cols] = preprocessing.scale(train[train_cols])
    #测试集数据
    query[train_cols] = preprocessing.scale(query[train_cols])

    #模型训练，并且打印出模型训练结果，这里全部使用的是默认参数。参数解释：https://blog.csdn.net/szlcw1/article/details/52336824
    print(clf.fit(train[train_cols], train['malicious']))

    # # 获取模型返回值
    # n_Support_vector = clf.n_support_  # 支持向量个数
    # Support_vector_index = clf.support_  # 支持向量索引
    # W = clf.coef_  # 方向向量W
    # b = clf.intercept_  # 截距项b

    # 绘制分类超平面
    # plot_point(train[train_cols], train['malicious'], Support_vector_index, W, b)

    #对模型的交叉验证得分，中文解释：https://blog.csdn.net/changzoe/article/details/78931214
    scores = cross_val_score(clf, train[train_cols], train['malicious'], cv=30)
    print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

    #对测试集进行预测
    print(query.keys())
    query['result'] = clf.predict(query[train_cols])

    #打印预测结果
    print(query[['URL', 'result']])


# Called from gui
# def forest_classifier_gui(train, query, train_cols):
#     rf = RandomForestClassifier(n_estimators=150)
#
#     print rf.fit(train[train_cols], train['malicious'])
#
#     query['result'] = rf.predict(query[train_cols])
#
#     print query[['URL', 'result']].head(2)
#     return query['result']


def forest_classifier(train, query, train_cols):
    #随机森林模型
    rf = RandomForestClassifier(n_estimators=200)

    #模型训练
    print(rf.fit(train[train_cols], train['malicious']))

    #交叉验证
    scores = cross_val_score(rf, train[train_cols], train['malicious'], cv=30)
    #打印交叉验证结果
    print('Estimated score RandomForestClassifier: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

    #预测
    query['result'] = rf.predict(query[train_cols])

    #打印预测结果
    print(query[['URL', 'result']])


#main.py中调用
def train(db, test_db):
    query_csv = pandas.read_csv(test_db)
    cols_to_keep, train_cols = return_nonstring_col(query_csv.columns)
    # query=query_csv[cols_to_keep]

    train_csv = pandas.read_csv(db)
    cols_to_keep, train_cols = return_nonstring_col(train_csv.columns)
    train = train_csv[cols_to_keep]
    svm_classifier(train_csv, query_csv, train_cols)

    #forest_classifier(train_csv, query_csv, train_cols)

#UI 暂时不用管
# def gui_caller(db, test_db):
#     query_csv = pandas.read_csv(test_db)
#     cols_to_keep, train_cols = return_nonstring_col(query_csv.columns)
#     # query=query_csv[cols_to_keep]
#
#     train_csv = pandas.read_csv(db)
#     cols_to_keep, train_cols = return_nonstring_col(train_csv.columns)
#     train = train_csv[cols_to_keep]
#
#     return forest_classifier_gui(train_csv, query_csv, train_cols)

def plot_point(dataArr, labelArr, Support_vector_index, W, b):
    for i in range(numpy.np.shape(dataArr)[0]):
        if labelArr[i] == 1:
            plt.scatter(dataArr[i][0], dataArr[i][1], c='b', s=20)
        else:
            plt.scatter(dataArr[i][0], dataArr[i][1], c='y', s=20)

    for j in Support_vector_index:
        plt.scatter(dataArr[j][0], dataArr[j][1], s=100, c='', alpha=0.5, linewidth=1.5, edgecolor='red')

    x = numpy.np.arange(0, 10, 0.01)
    y = (W[0][0] * x + b) / (-1 * W[0][1])
    plt.scatter(x, y, s=5, marker='h')
    plt.show()