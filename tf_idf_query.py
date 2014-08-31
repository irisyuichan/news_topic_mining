# -*- coding: utf-8 -*-
from pymongo import MongoClient
from operator import itemgetter
import jieba
client = MongoClient()
data = []
i = 0
for x in client.News.News.find():
  try:
    #fop = open('news_article/news_article_%d' % i, 'w')
    #fop.write(x['content'].encode('utf8'))
    data.append(x)
    i += 1
  except KeyError, TypeError:
    continue

"""
def list2freqdict(mylist):
    mydict=dict()
    for ch in mylist:
        mydict[ch]=mydict.get(ch,0)+1
    return mydict

def list2bigram(mylist):
    return [mylist[i:i+2] for i in range(0,len(mylist)-1)]

def list2trigram(mylist):
    return [mylist[i:i+3] for i in range(0,len(mylist)-2)]

def list2fourgram(mylist):
    return [mylist[i:i+4] for i in range(0,len(mylist)-3)]

def bigram2freqdict(mybigram):
    mydict=dict()
    for (ch1,ch2) in mybigram:
        mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
    return mydict

def trigram2freqdict(mytrigram):
    mydict=dict()
    for (ch1,ch2,ch3) in mytrigram:
        mydict[(ch1,ch2,ch3)]=mydict.get((ch1,ch2,ch3),0)+1
    return mydict

def fourgram2freqdict(myfourgram):
    mydict=dict()
    for (ch1,ch2,ch3,ch4) in myfourgram:
        mydict[(ch1,ch2,ch3,ch4)]=mydict.get((ch1,ch2,ch3,ch4),0)+1
    return mydict
"""
def freq2report(freqlist):
    chs=str()
    print('Char(s)\tCount')
    print('=============')
    for (token,num) in freqlist:
        for ch in token:
            chs=chs+ch
        print chs.encode('utf8') + '\t' + str(num)
        chs=''
    return
"""
sentence=reduce(lambda x,y: x + y['content'], data, u'')#data[0]['content']#u'吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮。'
chlist=[ch for ch in sentence]

chfreqdict=list2freqdict(chlist)
chbigram=list2bigram(chlist)
chtrigram=list2trigram(chlist)
chfourgram=list2fourgram(chlist)
bigramfreqdict=bigram2freqdict(chbigram)
trigramfreqdict=trigram2freqdict(chtrigram)
fourgramfreqdict=fourgram2freqdict(chfourgram)

chfreqsorted=sorted(chfreqdict.items(), key=itemgetter(1), reverse=True)
bigramfreqsorted=sorted(bigramfreqdict.items(), key=itemgetter(1), reverse=True)
trigramfreqsorted=sorted(trigramfreqdict.items(), key=itemgetter(1), reverse=True)
fourgramfreqsorted=sorted(fourgramfreqdict.items(), key=itemgetter(1), reverse=True)

freq2report(chfreqsorted[:10])
freq2report(bigramfreqsorted[:10])
freq2report(trigramfreqsorted[:10])
freq2report(fourgramfreqsorted[:10])
"""

from scipy.linalg import norm
import tfidf

def fast_cosine_sim(a, b):
    if len(b) < len(a):
        a, b = b, a

    up = 0
    for key, a_value in a.iteritems():
        b_value = b.get(key, 0)
        up += a_value * b_value
    if up == 0:
        return 0
    return up / norm(a.values()) / norm(b.values())

jieba.set_dictionary('dict.txt.big')

article_num = 2#len(data)

table = tfidf.tfidf()
words_table = dict()
#doc_count = []
for i in xrange(0, article_num):
  x = data[i]
  try:
    words = jieba.cut(x['content'], cut_all=False)
    words = [word for word in words]
    table.addDocument(i, words)
    words_table[i] = words
    #word_count = dict()
    #for word in words:
    #  word_count[word] = word_count.get(word, 0) + 1
    #doc_count.append(word_count)
    #print reduce(lambda x,y: x + '\n' + y, map(lambda (k,v): k + '\t' + str(v), word_count.items()))
  except:
    continue

print reduce(lambda x, y: x + ' ' + y, words_table[1])

#scores = dict()
#for i in xrange(0, article_num):
#  scores[i] = fast_cosine_sim(doc_count[0], doc_count[i])

#scoresorted=sorted(scores.items(), key=itemgetter(1), reverse=True)
#print reduce(lambda x,y: x + '\n' + y, map(lambda (k,v): str(k) + '\t' + str(v), scoresorted))

"""
select = [1, 384]
words_vector = []
for i in select:
  try:
    words_vector += words_table[i]
  except:
    continue
"""

tfidfsorted=sorted(table.similarities([u'復興',u'澎湖',u'航空',u'空難',u'颱風',u'家屬',u'班機',u'飛機',u'罹難者',u'天氣']), key=itemgetter(1), reverse=True)
print reduce(lambda x,y: x + '\n' + y, map(lambda (k,v): str(k) + '\t' + str(v), tfidfsorted))
#sentence=reduce(lambda x,y: x + y['content'], data, u'')#data[0]['content']#u'吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮。'

#words = jieba.cut(sentence, cut_all=False)

#print "Output 精確模式 Full Mode："
#for word in words:
#    print word
