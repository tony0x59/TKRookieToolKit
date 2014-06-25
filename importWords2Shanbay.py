#!/usr/bin/env python
# -*- coding: utf-8 -*-
"用于批量添加单词到扇贝的小工具"
"2014.6.25 Tony"

import requests
import time

class shanbay:

    host = "http://www.shanbay.com"
    target = "/bdc/vocabulary/add/batch/"
    url = host + target

    cookie = ''

    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"

    perSendWordsNum = 10

    words = []
    addedWords = []
    notFoundWords = []

    def __init__(self, cookie):
        self.cookie = cookie

    def headers(self):
        headers = {
            "Accept:": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.userAgent,
            "Referer": self.url,
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Cookie": self.cookie
        }
        return headers

    def addWords(self, words):
        if type(words) is list:
            self.words.extend(words)
        elif type(words) is str:
            self.words.append(words)

        # make sure words havn't overflow max 10
        num = self.perSendWordsNum
        if len(self.words) >= num:
            words = self.words[0:num]
            del self.words[0:num]
            self.sendRequest(words)

    def flush(self):
        if len(self.words) > 0:
            words = self.words
            self.words = []
            self.sendRequest(words)

    def sendRequest(self, words):
        assert(len(words) > 0 and len(words) <= self.perSendWordsNum)
        payload = {
            'words': words,
            '_': "%.0f" % (time.time() * 1000)
        }
        headers = self.headers()
        
        r = requests.get(self.url, params=payload, headers=headers)

        self.parseResult(r.json(), words)

    def parseResult(self, json, words):
        print 'rawJSON: ' + str(json)

        addedWords = []
        for word in json['learning_dicts']:
            addedWords.append(str(word['content']))
        
        notFoundWords = [val for val in words if val not in addedWords]

        #print 'added: ' + str(addedWords)
        #print 'notFound: ' + str(notFoundWords) 

        self.addedWords.extend(addedWords)
        self.notFoundWords.extend(notFoundWords)

    def addWordsFromFile(self, filename):
        count = 0
        with open(filename, 'r') as f:
            for word in f:
                self.addWords(word)
                #count += 1
                if count >= 20:
                    break
        self.flush()

def test():
    cookie = "csrftoken=z2RXYbmBVWhHVzaO6HZKhSZerSxrq0dF; sessionid=nic6i3ugacya74qykwl00ha8ngsah22g; username=tony7day; userid=2515219; __utma=183787513.2130683209.1403576157.1403576157.1403663984.2; __utmb=183787513.16.10.1403663984; __utmc=183787513; __utmz=183787513.1403576157.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E6%89%87%E8%B4%9D"

    s = shanbay(cookie)
    s.addWordsFromFile('words.txt')

    print '-' * 50
    print 'added: ' + str(s.addedWords)
    print '-' * 50
    print 'notFound: ' + str(s.notFoundWords) 

if __name__ == '__main__':
    test()
