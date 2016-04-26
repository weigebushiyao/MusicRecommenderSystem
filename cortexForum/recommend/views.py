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

from .models import Recommend

'''

'''
res = []
sim = []
url_title={}

result={}
check_result={}

user_graph_recommend={}
type_recommend={}

count=1335
know_way=1

like_70={
    '浮夸':'http://music.163.com/#/song?id=64886',
    '发誓':'http://music.163.com/#/song?id=331324',
    '文字流泪':'http://music.163.com/#/song?id=5243324',
    '最佳损友':'http://music.163.com/#/song?id=65800',
    '透明人间':'http://music.163.com/#/song?id=279108',
    '听到的神话':'http://music.163.com/#/song?id=279111',
    '谁可改变':'http://music.163.com/#/song?id=152266',
    '人来人往':'http://music.163.com/#/song?id=66378',
    '今生今世':'http://music.163.com/#/song?id=26620788',
    '海阔天空':'http://music.163.com/#/song?id=347230',
    '我只在乎你-邓丽君':'http://music.163.com/#/song?id=229010',
    '何日君再来-邓丽君':'http://music.163.com/#/song?id=226156',
    '但愿人长久-邓丽君':'http://music.163.com/#/song?id=225636',
}



like_80={
    '曲终人散-张宇':'http://music.163.com/#/song?id=190241',
    '趁早-张惠妹':'http://music.163.com/#/song?id=326997',
    '老情歌-李健':'http://music.163.com/#/song?id=5250148',
    '祝你一路顺风-吴奇隆':'http://music.163.com/#/song?id=5232855d',
    '往事随风-齐秦':'http://music.163.com/#/song?id=142580',
    '月亮代表我的心':'http://music.163.com/#/song?id=5264848',
    '上海滩':'http://music.163.com/#/song?id=111106',
    '爱你一万年':'http://music.163.com/#/song?id=25959710',
    '等待——汉武大帝主题曲':'http://music.163.com/#/song?id=4873688',
    '男儿当自强':'http://music.163.com/#/song?id=92428',
}

like_90={
    '庐州月':'http://music.163.com/#/song?id=167850',
    '清明雨上':'http://music.163.com/#/song?id=167882',
    '断桥残雪':'http://music.163.com/#/song?id=167937',
    '你若成风':'http://music.163.com/#/song?id=5299987',
    '七里香':'http://music.163.com/#/song?id=186001',
    '烟花易冷':'http://music.163.com/#/song?id=185668',
    '青花瓷':'http://music.163.com/#/song?id=185811',
    '蒲公英的约定':'http://music.163.com/#/song?id=185815',
    '黑色毛衣':'http://music.163.com/#/song?id=185908',
    '夜的第七章':'http://music.163.com/#/song?id=185878',
    '千里之外':'http://music.163.com/#/song?id=185880',
    '兰亭序':'http://music.163.com/#/song?id=185701',
}

like_00={
    '青春修炼手册':'http://music.163.com/#/song?id=28838718',
    '大梦想家':'http://music.163.com/#/song?id=33894380',
    '少年说':'http://music.163.com/#/song?id=35040843',
    '星空物语-TFBoys':'http://music.163.com/#/song?id=29716009',
    'IF-YOU BigBang':'http://music.163.com/#/song?id=32922450',
    'BAE BAR Bigbang':'http://music.163.com/#/song?id=31789299',
    'MAKE LOVE':'http://music.163.com/#/song?id=5366472',
    '다시 너를 (Liv)':'http://music.163.com/#/song?id=409646491',
}







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
        val1,val2,val3=request.POST.get('1',-1),request.POST.get('2',-1),request.POST.get('3',-1)
        val4,val5,val6=request.POST.get('4',-1),request.POST.get('5',-1),request.POST.get('6',-1)
        val7,val8,val9=request.POST.get('7',-1),request.POST.get('8',-1),request.POST.get('9',-1)
        val10=request.POST.get('10',-1)

        gender=int(request.POST.get('gender',0))
        birth_date=int(request.POST.get('birth_date',0))
        print 'gender{}'.format(gender)
        print 'birth_date{}'.format(birth_date)


        global user_graph_recommend
        if gender==0 or birth_date==0:
            user_graph_recommend={}
        elif  birth_date==2:
            #global like_80
            user_graph_recommend=like_70
        elif  birth_date==3:
            user_graph_recommend=like_80
        elif birth_date==4:
            user_graph_recommend=like_90
        elif gender==1 and birth_date==5:
            user_graph_recommend=like_90
        elif gender==2 and birth_date==5:
            user_graph_recommend=like_90

        global know_way
        know_way=request.POST.get('know_way',-1)


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
        global result
        result={
            'recommend_music':itemcf.result,
            'count':count,
            'test':test,
            'user_graph_recommend':user_graph_recommend
        }
        return HttpResponseRedirect(reverse('recommend_result'))
        #return render(request,'recommend/recommend_finalresult.html',result)

    return render(request, 'recommend/recommend_result.html', context)

def recommend_result(request):


    # 在这里的部分怎样写比较合适尼？
    print 123
    if request.method=='POST':
        satisfy_rate=request.POST.get('satisfy_rate')
        fresh_rate=request.POST.get('fresh_rate')
        recommend_check=Recommend(
            know_way=know_way,
            satisfy_rate=satisfy_rate,
            fresh_rate=fresh_rate
        )
        recommend_check.save()
        global check_result
        check_result={
                'fresh_rate':fresh_rate,
                'satisfy_rate_result':satisfy_rate,
                'count':Recommend.objects.count(),
                'datetime':Recommend.objects.values_list('pub_date').all(),
                'len':[i for i in xrange(Recommend.objects.values_list('pub_date').count())],
                'satisfy_rate_all':Recommend.objects.values_list('satisfy_rate',flat=True).all(),
                'fresh_rate_all':Recommend.objects.values_list('fresh_rate',flat=True).all(),
                'value2':Recommend.objects.filter(satisfy_rate__lte=2).count(),
                'value3':Recommend.objects.filter(satisfy_rate=3).count(),
                'value4':Recommend.objects.filter(satisfy_rate=4).count(),
                'value5':Recommend.objects.filter(satisfy_rate=5).count(),
                'value6':Recommend.objects.filter(know_way=1).count(),
                'value7':Recommend.objects.filter(know_way=2).count(),
                'value8':Recommend.objects.filter(know_way=3).count(),
        }
        return HttpResponseRedirect(reverse('recommend_result_check'))
    return render(request,'recommend/recommend_finalresult.html',result)

def recommend_result_check(request):


    return render(request,'recommend/recommend_result_check.html',check_result)