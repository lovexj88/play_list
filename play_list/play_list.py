__author__='aixj@aliyun.com'

import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np

def findCommonTracks(filenames):
    '''
    在播放列表中找到公共的曲目，并将它们保存在common.txt中
    :param filename:
    :return:
    '''
    trackNameSets = []
    for filename in filenames:
        #创建一个新的集合
        trackNames = set()
        #读取播放列表
        plist = plistlib.readPlist(filename)
        #得到曲目
        tracks = plist['Tracks']
        #迭代曲目
        for trackId, track in tracks.items():
            try:
                #将名字加入集合
                trackNameSets.add(track['Name'])
            except:
                pass
        #加入列表
        trackNameSets.append(trackNames)
    #的到公共的曲目
    commonTracks = set.intersection(*trackNameSets)
    #写入文件
    if len(commonTracks) > 0:
        f = open('common.txt', 'wb')
        for val in commonTracks:
            s = '%s\n'%val
            f.write(s.encode('utf-8'))
        f.close()
        print("%d 公共曲目没有找到" "曲目名字已经写到了 common.txt" %len(commonTracks))
    else:
        print("注意，没有公共的曲目！")

def plotStatus(filename):
    '''
    通过从播放列表中读取曲目信息绘制一些统计数据
    :param filename:
    :return:
    '''
    #读取播放列表
    plist = plistlib.readPlist(filename)
    #得到曲目
    tracks = plist['Tracks']
    #创建评级和持续时间列表
    ratings = []
    durations = []
    #迭代曲目
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Totle Time'])
        except:
            pass
    #确保收集有效的数据
    if ratings == [] or durations == []:
        print("在%s中没有有效的专辑评分/总时间数据."%filename)
        return

    #生成数组x
    x = np.array(durations, np.int32)
    #转换时间
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    #生成图像
    pyplot.show()

def findDuplicates(filename):
    '''
    在播放列表中寻找重复的曲目
    :param filename:
    :return:
    '''
    print('在%s中寻找重复的曲目'%filename)
    #读取播放列表
    plist = plistlib.readPlist(filename)
    #得到曲目
    tracks = plist['Tracks']
    #创建一个曲目字典
    trackNames = {}
    #迭代曲目
    for trackId, track in tracks.items():
        try:
            name = track['name']
            duration = track['Total Time']
            #判断是否已经存在
            if name in trackNames:
                #如果名称和持续时间匹配，则增加计数
                #时间四舍五入到最接近的秒
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                #把duration 和 count加入
                trackNames[name] = (duration, 1)
        except:
            pass
    #以(name, count)元组的形式存储重复的曲目
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    #保存dups到文件
    if len(dups) > 0:
        print("找到%d重复的，曲目的名字保存到了dup.txt中"%len(dups))
    else:
        print("没有找到重复的曲目！")
    f = open('dups.txt', 'w')
    for val in dups:
        f.write('[%d]%s\n'%(val[0], val[1]))
    f.close()

def main():
    #创建解析器
    descStr = '''
    该程序分析从iTunes导出的播放列表文件（.xml）
    '''
    parser = argparse.ArgumentParser(description=descStr)
    #添加一个互斥的参数组
    group = parser.add_mutually_exclusive_group()

    #添加参数
    group.add_argument('--common', nargs = '*', dest='plFiles', required=False)
    group.add_argument('--stats',dest='plFile', required=False)
    group.add_argument('--dup',dest='plFileD',required=False)

    #解析参数
    args = parser.parse_args()

    if args.plFiles:
        #找到公共的曲目
        findCommonTracks(args.plFiles)
    elif args.plFile:
        #打分的意思吧
        plotStatus(args.plFile)
    elif args.plFileD:
        #找到重复的曲目
        findDuplicates(args.plFileD)
    else:
        print('这些不是你正在寻找的曲目')

if __name__=='__main__':
    main()









