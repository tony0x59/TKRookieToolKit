# -*- coding: utf8 -*-

#!/usr/bin/env python

"""
监测网络状态 当网络可用时，发出提示音
需要用到一个命令行播放MP3的小程序：mpg123
brew install mpg123

made by tony 2013.7.28
"""

import urllib2
import time
import os

testurl = 'http://www.taobao.com'

def internet_on():
    try:
        response = urllib2.urlopen(testurl, timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

succNum = 0

while True:
	if internet_on():
		succNum += 1
		print 'test conn success [%d]'%succNum
		if succNum > 5:
			os.popen('mpg123 -q dingding.mp3')
	else:
		print 'test conn false'
		succNum = 0

	time.sleep(3)
