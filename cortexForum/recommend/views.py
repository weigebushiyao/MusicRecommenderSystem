# -*- coding:utf-8 -*-
from __future__ import division
from operator import itemgetter
import math
import os
import base64
import random

current_path = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(current_path, 'base.txt')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

'''

'''
res = []
sim = []
url_title={}

count=1335
# 维护一个用 dict 表示的 相似矩阵
class ItemBasedCF(object):
    def __init__(self, trainFilename):
        self.trainset = self.loadFile(trainFilename)
        self.K = 5
        self.N = 40



    def changeParama(self, K, N):
        self.K = K
        self.N = N

    @staticmethod
    def loadFile(filename):
        content = {}
        with open(filename, 'r') as f:
                f=[line.strip() for line in f if line.strip()]
                global count
                count=int(f[-1].split()[0])
                print count
                for line in f:
                    userID, movieID,url,rating = line.split()
                    url_title[movieID]=url
                    content.setdefault(int(userID), {})[movieID] = int(rating)

        return content

    def calSimilarity(self):
        # 计算矩阵相似度

        trainset = self.trainset
        counter = {}
        simMatrix = {}

        for userID, items in trainset.items():
            for i in items:
                counter.setdefault(i, 0)
                counter[i] += 1

                simitems = simMatrix.setdefault(i, {})
                for j in items:
                    if not i == j:
                        simitems.setdefault(j, 0)
                        simitems[j] += 1

        for i, simitems in simMatrix.items():
            for j in simitems:
                simMatrix[i][j] /= math.sqrt(counter[i] * counter[j])

        self.simMatrix = simMatrix
        global sim
        sim = simMatrix

    def generateRandomSong(self):
        trainset=self.trainset
        randomsong=[]
        for index in [random.randint(1,3611) for i in range(10)]:
            randomsong.extend(trainset[index].keys())
        self.originsong=[song for song in randomsong][:10]
        randomsong_url=[url_title[song] for song in self.originsong]
        randomsong=[base64.b64decode(song) for song in self.originsong]

        randomsong=list(set(randomsong))
        self.randomsong=randomsong
        self.randomsong_url=randomsong_url



    def calRecommendation(self):
        #  进行 K,N 推荐
        simMatrix = self.simMatrix
        trainset = self.trainset
        K = self.K
        N = self.N
        self.resset = {}

        for userID in trainset:
            rank = {}
            items = trainset.get(userID)

            for i, rating in items.items():
                simitems = simMatrix.get(i)

                if not simitems:
                    continue
                for j, simIJ in sorted(simitems.items(), key=itemgetter(1), reverse=True)[:K]:
                    if not j in items:
                        rank.setdefault(j, 0)
                        rank[j] += simIJ * rating

            if len(rank) < N:
                self.resset[userID] = rank

            res = {}
            for itemID, rating in sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]:
                res[itemID] = rating

            self.resset[userID] = res
        global res
        res = self.resset

    def re(self):
        self.result = self.resset.get(sorted(self.trainset.keys())[-1])
        #print sorted(self.trainset.keys())[-1]
        target=[]
        for temp in self.result:
            target.append(base64.b64decode(temp))
        self.result=target


    def recall(self):
        # 计算召回率
        pass


def itemRecommend(request):
    itemcf = ItemBasedCF(file_path)
    itemcf.generateRandomSong()
    test=[1,2,3,4,5]

    context = {
        'random_song':itemcf.randomsong,
        'random_song_url':itemcf.randomsong_url,
        'test':test,
    }
    if request.method=='POST':
        val1,val2,val3=request.POST.get('1'),request.POST.get('2'),request.POST.get('3')
        global count
        count+=1
        userid=count

        with open(file_path, 'a') as f:

            f.writelines(str(userid)+' '+itemcf.originsong[0]+' '+ 'None' + ' '+str(val1)+'\n')
            f.writelines(str(userid)+' '+itemcf.originsong[1]+' '+ 'None' + ' '+str(val2)+'\n')
            f.writelines(str(userid)+' '+itemcf.originsong[2]+' '+ 'None' + ' '+str(val3)+'\n')
        itemcf.trainset=itemcf.loadFile(file_path)
        '''
        userid=sorted(itemcf.trainset.keys())[-1]+1
        new_ele={}


        itemcf.trainset[int(userid)]={itemcf.randomsong[0]:val1,itemcf.randomsong[1]:val2,itemcf.randomsong[2]:val3}
        '''
        itemcf.calSimilarity()
        itemcf.calRecommendation()
        itemcf.re()
        global count
        test=[12,3,4,5]
        result={
            'recommend_music':itemcf.result,
            'count':count,
            'test':test,
        }
        return render(request,'recommend/recommend_finalresult.html',result)

    return render(request, 'recommend/recommend_result.html', context)

def recommend_result(request):

    if request.method=='POST':
        pass  # 在这里的部分怎样写比较合适尼？

    return render(request,'recommend/recommend_finalresult.html',result)