'''
    Function: aria_down
    Descrption: 封装aria2c下载工具
    Author: Tony
    Date: 2012.06.13

    注意：此命令适用于Windows下命令行调用，Linux下调用需要将aria参数中的 " 修改为 '
'''

import os

'''
    参数说明：
    url  下载地址，可以是单个地址，也可是列表
    path 下载文件的存放目录，默认存放到当前程序执行目录
    proxy 使用HTTP代理，默认使用本机GAE
    useragent 设置User-Agent信息
    curt_max 最多同时下载文件个数
    split 单个下载文件的分割数
'''
def aria_down(url, path=None, curt_max=1, split=5,
              proxy='http://127.0.0.1:8087',
              useragent=None):
    
    dl_list = 'dl_list.txt'
    if os.path.exists(dl_list) == True:
        os.remove(dl_list)

    #将下载文件列表写入txt文件
    try:
        with open(dl_list, 'w') as f:
            if isinstance(url, list):
                for i in url:
                    f.write(i + '\n')
            else:
                f.write(url + '\n')
    except IOError as err:
        print('File error:' + str(err))

    #生成下载命令
    command = 'aria2c -j' + str(curt_max) + ' -s' + str(split)
    if path != None:
        command += ' --dir="' + path + '"'
    if proxy != None:
        command += ' --http-proxy="' + proxy + '"'
    if useragent != None:
        command += ' --user-agent="' + useragent + '"'
    command += ' -i "' + dl_list + '"'

    print(command)
    
    #调用aria2c进行下载
    os.system(command)

