#!/usr/bin/python
# -*- coding:utf8 -*-
from urllib.parse import urlparse
import re
import urllib
from xml.dom import minidom
import csv
import pygeoip
from numpy import unicode

nf = -1

#[average len, number of words, longest word]
def Tokenise(url):
        if url == '':
            return [0, 0, 0]
        token_word = re.split('\W+', url)
        #print token_word
        no_ele = sum_len = largest = 0
        for ele in token_word:
                l = len(ele)
                sum_len += l
                if l > 0: ## for empty element exclusion in average length
                        no_ele += 1
                if largest < l:
                        largest = l
        try:
            return [float(sum_len)/no_ele, no_ele, largest]
        except:
            return [0, no_ele, largest]


#
def find_ele_with_attribute(dom, ele, attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return nf
        

# 网站流行度，这是Amazon的API，已经过时了，需要修改，先注释掉
# def sitepopularity(host):
#
#         xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
#         #print xmlpath
#         try:
#             xml= urllib2.urlopen(xmlpath)
#             dom =minidom.parse(xml)
#             rank_host=find_ele_with_attribute(dom,'REACH','RANK')
#             #country=find_ele_with_attribute(dom,'REACH','RANK')
#             rank_country=find_ele_with_attribute(dom,'COUNTRY','RANK')
#             return [rank_host,rank_country]
#
#         except:
#             return [nf,nf]


# 判断URL里面单词的敏感程度
def Security_sensitive(tokens_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin']
    cnt=0
    for ele in sec_sen_words:
        if (ele in tokens_words):
            cnt += 1

    return cnt


#判断有没有.exe
def exe_in_url(url):
    if url.find('.exe') != -1:
        return 1
    return 0


#检查URL里有没有IP地址
def Check_IPaddress(tokens_words):
    cnt = 0
    for ele in tokens_words:
        if unicode(ele).isnumeric():
            cnt += 1
        else:
            if cnt >= 4:
                return 1
            else:
                cnt = 0
    if cnt >= 4:
        return 1
    return 0


#暂时不知道这里面是啥 - 好像是获取在哪个国家
def getASN(host):
    try:
        g = pygeoip.GeoIP('GeoIPASNum.dat')
        asn = int(g.org_by_name(host).split()[0][2:])
        return asn
    except:
        return nf


#
# def web_content_features(url):
#     #这是一个字典（理解成HashMap），存放网页特征的
#     wfeatures = {}
#     total_cnt = 0
#     try:
#         source_code = str(opener.open(url)) #获取这个URL对应页面的URL源码
#         #print source_code[:500]
#
#         wfeatures['src_html_cnt'] = source_code.count('<html') #多少个html标签
#         wfeatures['src_hlink_cnt'] = source_code.count('<a href=') #多少个超链接
#         wfeatures['src_iframe_cnt'] = source_code.count('<iframe') #
#
#         #suspicioussrc_ javascript functions count -> 这边是看有多少可疑的javascript函数
#         wfeatures['src_eval_cnt'] = source_code.count('eval(')
#         wfeatures['src_escape_cnt'] = source_code.count('escape(')
#         wfeatures['src_link_cnt'] = source_code.count('link(')
#         wfeatures['src_underescape_cnt'] = source_code.count('underescape(')
#         wfeatures['src_exec_cnt'] = source_code.count('exec(')
#         wfeatures['src_search_cnt'] = source_code.count('search(')
#
#         #看看这个URL对应页面中可疑的JavaScript函数有多少个
#         for key in wfeatures:
#             if key != 'src_html_cnt' and key != 'src_hlink_cnt' and key != 'src_iframe_cnt':
#                 total_cnt += wfeatures[key]
#         wfeatures['src_total_jfun_cnt'] = total_cnt
#
#     #打不开这个URL，所有的特征对应的值都为1
#     except Exception as e:
#         print("Error" + str(e) + " in downloading page " + url)
#         default_val = nf
#
#         wfeatures['src_html_cnt'] = default_val
#         wfeatures['src_hlink_cnt'] = default_val
#         wfeatures['src_iframe_cnt'] = default_val
#         wfeatures['src_eval_cnt'] = default_val
#         wfeatures['src_escape_cnt'] = default_val
#         wfeatures['src_link_cnt'] = default_val
#         wfeatures['src_underescape_cnt'] = default_val
#         wfeatures['src_exec_cnt'] = default_val
#         wfeatures['src_search_cnt'] = default_val
#         wfeatures['src_total_jfun_cnt'] = default_val
#
#     return wfeatures


# 这是Google的API，已经过时了，需要修改，先注释掉
# def safebrowsing(url):
#     api_key = "ABQIAAAA8C6Tfr7tocAe04vXo5uYqRTEYoRzLFR0-nQ3fRl5qJUqcubbrw"
#     name = "URL_check"
#     ver = "1.0"
#
#     req = {}
#     req["client"] = name
#     req["apikey"] = api_key
#     req["appver"] = ver
#     req["pver"] = "3.0"
#     req["url"] = url #change to check type of url
#
#     try:
#         params = urllib.urlencode(req)
#         req_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?"+params
#         res = urllib2.urlopen(req_url)
#         # print res.code
#         # print res.read()
#         if res.code == 204:
#             # print "safe"
#             return 0
#         elif res.code == 200:
#             # print "The queried URL is either phishing, malware or both, see the response body for the specific type."
#             return 1
#         elif res.code == 204:
#             print "The requested URL is legitimate, no response body returned."
#         elif res.code == 400:
#             print "Bad Request The HTTP request was not correctly formed."
#         elif res.code == 401:
#             print "Not Authorized The apikey is not authorized"
#         else:
#             print "Service Unavailable The server cannot handle the request. Besides the normal server failures, it could also indicate that the client has been throttled by sending too many requests"
#     except:
#         return -1


#这个函数调用了上面的所有函数，组建最后的特征Feature(这也是个字典<特征，值>)
#这函数最终是在main函数里面调用的
def getFeatures(url_input):

        Feature = {}
        tokens_words = re.split('\W+', url_input)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
        #print tokens_words,len(tokens_words)

        #token_delimit1=re.split('[./?=-_]',url_input)
        #print token_delimit1,len(token_delimit1)

        obj = urlparse(url_input)
        host = obj.netloc
        path = obj.path

        Feature['URL'] = url_input

        #暂时先注释掉
        #Feature['rank_host'], Feature['rank_country'] = sitepopularity(host)

        Feature['host'] = obj.netloc
        Feature['path'] = obj.path

        Feature['Length_of_url'] = len(url_input)
        Feature['Length_of_host'] = len(host)
        Feature['No_of_dots'] = url_input.count('.')

        Feature['avg_token_length'], Feature['token_count'], Feature['largest_token'] = Tokenise(url_input)
        Feature['avg_domain_token_length'], Feature['domain_token_count'], Feature['largest_domain'] = Tokenise(host)
        Feature['avg_path_token'], Feature['path_token_count'], Feature['largest_path'] = Tokenise(path)

        Feature['sec_sen_word_cnt'] = Security_sensitive(tokens_words)
        Feature['IPaddress_presence'] = Check_IPaddress(tokens_words)
        
        # print host
        # print getASN(host)
        # Feature['exe_in_url']=exe_in_url(url_input)
        Feature['ASNno'] = getASN(host)
        #Feature['safebrowsing'] = safebrowsing(url_input)
        """wfeatures=web_content_features(url_input)
        
        for key in wfeatures:
            Feature[key]=wfeatures[key]
        """
        #debug
        # for key in Feature:
        #     print key +':'+str(Feature[key])
        return Feature