#!/usr/bin/python
# -*- coding:utf8 -*-

import ipaddress as ip
from os.path import splitext
from urllib.parse import urlparse
import tldextract

Suspicious_TLD = ['zip', 'cricket', 'link', 'work', 'party', 'gq', 'kim', 'country', 'science', 'tk']
Suspicious_Domain = ['luckytime.co.kr', 'mattfoll.eu.interia.pl', 'trafficholder.com', 'dl.baixaki.com.br',
                     'bembed.redtube.comr', 'tags.expo9.exponential.com', 'deepspacer.com', 'funad.co.kr',
                     'trafficconverter.biz']


# Method to count number of dots
def countdots(url):
    return url.count('.')


# Method to count number of delimeters
def countdelim(url):
    count = 0
    delim = [';', '_', '?', '=', '&']
    for each in url:
        if each in delim:
            count = count + 1
    return count


# Is IP addr present as th hostname, let's validate
def isip(uri):
    try:
        if ip.ip_address(uri):
            return 1
    except:
        return 0


# method to check the presence of hyphens
def isPresentHyphen(url):
    return url.count('-')


# method to check the presence of @
def isPresentAt(url):
    return url.count('@')


def isPresentDSlash(url):
    return url.count('//')

def countSubDir(url):
    return url.count('/')


def get_ext(url):
    """Return the filename extension from url, or ''."""
    root, ext = splitext(url)
    return ext

def countSubDomain(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))

def countQueries(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))

def getFeatures(url):
    result = {}
    url = str(url)

    # add the url to feature set
    result['URL'] = url

    # parse the URL and extract the domain information
    path = urlparse(url)
    ext = tldextract.extract(url)

    # counting number of dots in subdomain
    result['DOTS_OF_SUB_DOMAIN'] = countdots(ext.subdomain)

    # checking hyphen in domain
    result['HAS_HYPHEN'] = isPresentHyphen(path.netloc)

    # length of URL
    result['LEN_OF_URL'] = len(url)

    # checking @ in the url
    result['HAS_AT_SIGN'] = isPresentAt(path.netloc)

    # checking presence of double slash
    result['HAS_DOUBLE_SLASH'] = isPresentDSlash(path.path)

    # Count number of subdir
    result['NUM_OF_SUBDIR'] = countSubDir(path.path)

    # number of sub domain
    result['NUM_OF_SUB_DOMAIN'] = countSubDomain(ext.subdomain)

    # length of domain name
    result['LEN_OF_DOMAIN_NAME'] = len(path.netloc)

    # count number of queries
    result['NUM_OF_QUERIES'] = len(path.query)

    # Adding domain information

    # if IP address is being used as a URL
    result['DOMAIN_IS_IP'] = isip(ext.domain)

    # presence of Suspicious_TLD
    result['SUSPICIOUS_TLD'] = 1 if ext.suffix in Suspicious_TLD else 0

    # presence of suspicious domain
    result['SUSPICIOUS_DOMAIN'] = 1 if '.'.join(ext[1:]) in Suspicious_Domain else 0

    # result.append(get_ext(path.path))

    return result
