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

user_type_recommend={}

yue_chinese_song={
    '红日':'http://music.163.com/#/song?id=115502',
    '海阔天空':'http://music.163.com/#/song?id=347230',
    '富士山下':'http://music.163.com/#/song?id=65766',
    '人来人往':'http://music.163.com/#/song?id=65624',
    '光辉岁月':'http://music.163.com/#/song?id=346576',
    '沉默是金':'http://music.163.com/#/song?id=188204',
    '只想一生跟你走':'http://music.163.com/#/song?id=189987'
}

europe_song={
    'Emily-San Fermilin':'http://music.163.com/#/song?id=31517702',
    'Talking to myself-SoySauce':'http://music.163.com/#/song?id=33984810',
    'flood on the floor':'http://music.163.com/#/song?id=30512373',
    'Rihanna-Clean Ban':'http://music.163.com/#/song?id=30967523',
    'Silver lining-Hurts':'http://music.163.com/#/song?id=4112003',
    'Invisible-Kid Astray':'http://music.163.com/#/song?id=32683910',
    'The beautiful ones-Monarchy':'http://music.163.com/#/song?id=29307030',
}

japan_song={
    'あなたに出会わなければ~夏雪冬花~':'http://music.163.com/#/song?id=560079',
    'farewill':'http://music.163.com/#/song?id=22816399',
    '最後のわがまま':'http://music.163.com/#/song?id=33346908',
    '群青 ~album mix - remix -阿部芙蓉美':'http://music.163.com/#/song?id=22713385',
    '君に贈る歌 ~Song For You -Che\'Nelle':'http://music.163.com/#/song?id=30590210',
}

dj_song={
    'Rocky(Kaaze\'s Extended Mix)-  Tiësto / Kaaze':'http://music.163.com/#/song?id=33760006',
    'Clap Your Hands (Original Mix)-David Guetta / Glowinthedark':'http://music.163.com/#/song?id=35253632',
    'How Deep Is Your Love (Radio Edit)-Calvin Harris':'http://music.163.com/#/song?id=33668983',
    'How We Party (Original Mix)-R3hab':'http://music.163.com/#/song?id=28870241',
    'On My Mind (Radio Edit)-Don Diablo':'http://music.163.com/#/song?id=33054022',
    'Savior (Original Mix) - Bassjackers':'http://music.163.com/#/song?id=29535451',
}

traditional_song={
    'Johann Strauss II: Rosen aus dem Süden, Walzer, Op. 388-Wiener Philharmoniker':'http://music.163.com/#/song?id=35470320',
    'Symphony No. 40 in G Minor, K. 550- I. Allegro molto-Wolfgang Amadeus Mozart':'http://music.163.com/#/song?id=27256788',
    'Paganini – Moto perpetuo Op. 11 – M. Rabin 帕格尼尼:无穷动':'http://music.163.com/#/song?id=5105993',
    'Gaspard De La Nuit, 3 Poèmes Pour Piano D\'après Aloysius Bertrand : Ondine (Remasterisé En 2010)':'http://music.163.com/#/song?id=22380369',
    'Sonata for Piano and Violin in E minor, K.304, Temp di Menuetto':'http://music.163.com/#/song?id=26935413',
    '梦里水乡':'http://music.163.com/#/song?id=5266956',
    '春江花月夜-袁莎':'http://music.163.com/#/song?id=322470',
    'Romance for Cello':'http://music.163.com/#/song?id=26500528',

}
electric_song={
    'Go Time-Mark Petrie':'http://music.163.com/#/song?id=29717271',
    'Shadows-Janji':'http://music.163.com/#/song?id=31830308',
    'Faded (Instrumental)-Alan Walker':'http://music.163.com/#/song?id=36990267',
    'Purple Passion -：Diana Boncheva':'http://music.163.com/#/song?id=2529472',
    'Evolving - Ahrix':'http://music.163.com/#/song?id=32192216',
    'Becoming a Legend - John Dreamer':'http://music.163.com/#/song?id=28283167',
    'Daybreak (GoPro HERO3 Edit) - Overwerk':'http://music.163.com/#/song?id=28592966',
    '七剑战歌 - ：川井憲次':'http://music.163.com/#/song?id=30474386',

}

mental_song={
    'Everything Sucks - Dope':'http://music.163.com/#/song?id=17266068',
    'You Spin Me Round (Like a Record) - Dope':'http://music.163.com/#/song?id=5054358',
    'Blood-Stained (Give Me Your Body) - Project Pitchfork':'http://music.163.com/#/song?id=29412010',
    'Hass Mich..Lieb Mich - Stalhman':'http://music.163.com/#/song?id=19180696',
    'Deaf, Dumb and Blind - Godflesh':'http://music.163.com/#/song?id=4087708',
    'Critical Acclaim (Album Version) - Avenged Sevenfold':'http://music.163.com/#/song?id=20503624',
    'Bad Blood(黑客帝国) - ：Ministry':'http://music.163.com/#/song?id=5054967',
}

pure_song={
    'Cold Winter':'http://music.163.com/#/song?id=33495597',
    '白昼之夜 - 林隆璇':'http://music.163.com/#/song?id=116493',
    '雨空 - α~pav':'http://music.163.com/#/song?id=139206',
    'Righteous Path - Blazo':'http://music.163.com/#/song?id=5101648',
    'Snowdream 雪之梦 - 班得瑞':'http://music.163.com/#/song?id=3951353',
    'Mariage d\' manour 梦中的婚礼 理查德克莱德曼':'http://music.163.com/#/song?id=5038302',
    'Exodus - 马克西姆.姆尔维察':'http://music.163.com/#/song?id=1696336',
    'Nature\'s Path 自然小径':'http://music.163.com/#/song?id=1220787',

}

chinese_song={
    '空谷幽兰 - 许巍':'http://music.163.com/#/song?id=25657380',
    '东风破 - 周杰伦':'http://music.163.com/#/song?id=186018',
    '江南 - 林俊杰':'http://music.163.com/#/song?id=108914',
    '红颜 - 胡彦斌':'http://music.163.com/#/song?id=93213',
    '红尘客栈 - 周杰伦':'http://music.163.com/#/song?id=25641368',
    '烟花易冷 - 周杰伦':'http://music.163.com/#/song?id=185668',
    '此生不换 - ':'http://music.163.com/#/song?id=86363',

}

# maintain the matrix represented by dict
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
        """
        calculate the complexity
        """

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
        #  recommend K,N
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
        pass


def itemRecommend(request):
    itemcf = ItemBasedCF(file_path)
    itemcf.generateRandomSong()
    test=[1,2,3,4,5]
    w=dict(zip(itemcf.randomsong,itemcf.randomsong_url))
    #w={ keys:url_title[keys] for keys in itemcf.randomsong.keys()}
    context = {
        #'random_song':itemcf.randomsong,
        #'random_song_url':itemcf.randomsong_url,
        'random_song':w,
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
        user_graph_recommend={}
        if gender==1 and birth_date==1:
            user_graph_recommend={}
        elif birth_date==2:
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

        global user_type_recommend
        user_type_recommend={}
        type_like=request.POST.getlist('type_like')
        print type_like
        type_like=[int(item) for item in type_like]
        if 1 in type_like:
            for music in random.sample(yue_chinese_song.keys(),3):
                user_type_recommend[music]=yue_chinese_song[music]
        if 3 in type_like:
            for music in random.sample(europe_song.keys(),3):
                user_type_recommend[music]=europe_song[music]
        if 4 in type_like:
            for music in random.sample(japan_song.keys(),3):
                user_type_recommend[music]=japan_song[music]
        if 5 in type_like:
            for music in random.sample(dj_song.keys(),3):
                user_type_recommend[music]=dj_song[music]
        if 6 in type_like:
            for music in random.sample(traditional_song.keys(),3):
                user_type_recommend[music]=traditional_song[music]
        if 7 in type_like:
            for music in random.sample(electric_song.keys(),3):
                user_type_recommend[music]=electric_song[music]
        if 8 in type_like:
            for music in random.sample(mental_song.keys(),3):
                user_type_recommend[music]=mental_song[music]
        if 9 in type_like:
            for music in random.sample(pure_song.keys(),3):
                user_type_recommend[music]=pure_song[music]
        if 10 in type_like:
            for music in random.sample(pure_song.keys(),3):
                user_type_recommend[music]=pure_song[music]
        if 11 in type_like:
            for music in random.sample(electric_song.keys(),3):
                user_type_recommend[music]=electric_song[music]
        if 12 in type_like:
            for music in random.sample(chinese_song.keys(),3):
                user_type_recommend[music]=chinese_song[music]


        print user_type_recommend



        global count
        count+=1
        userid=count

        with open(file_path, 'a') as f:
            if val1 not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[0]+' '+ 'None' + ' '+str(val1)+'\n')
            if val2  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[1]+' '+ 'None' + ' '+str(val2)+'\n')
            if val3  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[2]+' '+ 'None' + ' '+str(val3)+'\n')
            if val4  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[3]+' '+ 'None' + ' '+str(val4)+'\n')
            if val5  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[4]+' '+ 'None' + ' '+str(val5)+'\n')
            if val6  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[5]+' '+ 'None' + ' '+str(val6)+'\n')
            if val7  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[6]+' '+ 'None' + ' '+str(val7)+'\n')
            if val8  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[7]+' '+ 'None' + ' '+str(val8)+'\n')
            if val9  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[8]+' '+ 'None' + ' '+str(val9)+'\n')
            if val10  not in (0,-1):
                f.writelines(str(userid)+' '+itemcf.originsong[9]+' '+ 'None' + ' '+str(val10)+'\n')
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
            'user_graph_recommend':user_graph_recommend,
            'user_type_recommend':user_type_recommend,
        }
        return HttpResponseRedirect(reverse('recommend_result'))
        #return render(request,'recommend/recommend_finalresult.html',result)

    return render(request, 'recommend/recommend_result.html', context)

def recommend_result(request):
    
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
                'value9':Recommend.objects.filter(fresh_rate__lte=2).count(),
                'value10':Recommend.objects.filter(fresh_rate=3).count(),
                'value11':Recommend.objects.filter(fresh_rate=4).count(),
                'value12':Recommend.objects.filter(fresh_rate=5).count(),
        }
        return HttpResponseRedirect(reverse('recommend_result_check'))
    return render(request,'recommend/recommend_finalresult.html',result)

def recommend_result_check(request):


    return render(request,'recommend/recommend_result_check.html',check_result)