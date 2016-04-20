# -*- coding:utf-8 -*-
from __future__ import division
from operator import itemgetter
import math
import os
import base64

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
            for line in f:
                if not line:
                    continue
                userID, movieID, rating = line.split()
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
        self.result = self.resset.get(2)
        target=[]
        for temp in self.result:
            target.append(base64.b64decode(temp))
        self.result=target


    def recall(self):
        # 计算召回率
        pass


def itemRecommend(request):
    itemcf = ItemBasedCF(file_path)
    itemcf.calSimilarity()
    itemcf.calRecommendation()
    itemcf.re()
    context = {
        'recommend_music': itemcf.result,

    }

    return render(request, 'recommend/recommend_result.html', context)
