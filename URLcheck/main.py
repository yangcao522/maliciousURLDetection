#!/usr/bin/python
# -*- coding:utf8 -*-

import csv
# import URLcheck.Feature_extraction as urlfeature2
import URLcheck.Feature_extraction2 as urlfeature2
import URLcheck.trainer as tr
import URLcheck.trainer2 as tr2

def resultwriter(feature, output_dest):
    flag=True
    with open(output_dest, 'w') as f:
        for item in feature:
            w = csv.DictWriter(f, item[1].keys())
            if flag:
                w.writeheader()
                flag = False
            w.writerow(item[1])

def process_URL_list(file_dest, output_dest):
    feature = []
    with open(file_dest) as file:
        i = 0
        for line in file:
            i = i + 1
            url = line.split(',')[0].strip()
            malicious_bool = line.split(',')[1].strip()
            if url != '':
                #rint 'working on: ' + url#showoff
                ret_dict = urlfeature2.getFeatures(url)
                ret_dict['malicious'] = malicious_bool
                feature.append([url, ret_dict])
            if i == 2000:
                break
    resultwriter(feature, output_dest)

def process_test_list(file_dest, output_dest):
    feature = []
    with open(file_dest) as file:
        for line in file:
            url = line.strip()
            if url != '':
                print('working on: ' + url)  # showoff
                ret_dict = urlfeature2.getFeatures(url)
                feature.append([url, ret_dict])
    resultwriter(feature, output_dest)

#change
def process_test_url(url, output_dest):
    feature = []
    url = url.strip()
    if url != '':
        print('working on: ' + url)  # showoff
        ret_dict = urlfeature2.getFeatures(url)
        feature.append([url, ret_dict])
    resultwriter(feature, output_dest)


# def main():
#process_URL_list('phish_test2000.txt', 'url_features.csv')
# process_test_list("query.txt", 'query_features.csv')
#tr.train('url_features.csv', 'url_features.csv')         #arguments:(input_training feature, test/query traning features)
# tr.train('url_features.csv', 'query_features.csv')      #testing with urls in query.txt
tr2.train('url_features.csv')