# -*- coding: latin-1 -*-

import sys
import os
import numpy as np
import datetime

from nltk.corpus import machado as mch
import nltk
from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
from   Topics.visualization.wordcloud import make_wordcloud
from IPython.display import display, Image
import glob


import logging as log

FONT_PATH = 'C:\Windows\Fonts\Arial.ttf'


logFormatter = log.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = log.getLogger()

fileHandler = log.FileHandler("{0}/{1}.log".format('./', 'log.txt'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = log.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


reload(sys)
sys.setdefaultencoding("utf-8")

def nomes_documentos(pasta):
    return os.listdir(pasta+'/tokens')

def stopwords_en():
    f = open('stopwords_en.txt','r')
    stopw = f.read().split('\n')
    f.close()
    return stopw


def stopwords_pt():
    f = open('stopwords_pt.txt','r')
    stopw = f.read().split('\n')
    f.close()
    return stopw

def cria_pastas(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    dirs = [pasta+'/tokens',pasta+'/freq',pasta+'/vocab']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def pre_processamento(pasta, nltk_corpus, stopwords, min_rep=10):
    
    for fileid in nltk_corpus.fileids():
        t1 = datetime.datetime.now()
        print 'Tokenizar %s...' % fileid 
        
        # Carrega todas as palavras.
        words = nltk_corpus.words(fileid)
        
        # Filtra palavras menores que 3 caracteres e stopwords.
        doc = [w.lower() for w in words if len(w) > 3 and  w.lower() not in stopwords]

        # Filtra palavras que aparecem menos de 10 vezes.
        fd = nltk.FreqDist(doc)
        if min_rep > 0 :
            doc = [w for w in doc if fd[w] > min_rep]
       
            if len(doc) == 0:
                raise Exception ('Filtro com {} palaras repetidas diminuou bastatnte o vocabulario.'.format(min_rep))

        # Salva palavras em um novo documentos.
        f = open(pasta+'/tokens/'+fileid.replace('/','_'),'w')
        for w in doc:
            f.write(w+u'\n')
        f.close()
        delta_t = datetime.datetime.now()-t1
        print 'Tokenizado  ''%s'' em %d segundos.'%(fileid, delta_t.seconds) 

        
def registra_freq(pasta):
    for i in nomes_documentos(pasta):
        fdoc = open(pasta+'/tokens/' + i,'r')
        doc = fdoc.read().split('\n')
        fdoc.close()
        fd = nltk.FreqDist(doc)
        ffreq = open(pasta+'/freq/'+i, 'w')
        for k,v in fd.items():
            ffreq.write(k+';'+str(v)+'\n')
        ffreq.close()
        
        

def constroi_vocabulario(pasta):
    items = None
    vocab = set([])
    palavras = []
    for arqv in os.listdir(pasta+'/freq'):
        f = open(pasta+'/freq/'+arqv, 'r')
        items = f.read().split('\n')
        f.close()
        lista = []
        for i in items:
            word = i.split(';')[0]
            lista.append(word)
            palavras.append(word)
        vocab = set(list(vocab)+lista)
    f = open(pasta+'/vocab/vocab.txt','w')
    txt = '\n'.join(sorted(vocab))
    f.write(txt)
    f.close()

    # Registra a ocorrência das palavras entre os documentos.
    fd = nltk.FreqDist(palavras)
    ffreq = open(pasta+'/palavras_comuns.txt','w')
    for k,v in fd.items():
        ffreq.write(k+';'+str(v)+'\n')
    ffreq.close()

def palavras_comuns(pasta):    
    f = open(pasta+'/palavras_comuns.txt', 'r')
    txt = f.read().splitlines()
    f.close()
    return txt


def vocabulario(pasta):
    f = open(pasta+'/vocab/vocab.txt', 'r')
    txt = f.read().splitlines()
    f.close()
    return txt

def documentos(pasta):
    arqvs = os.listdir(pasta+'/tokens')
    docs = []
    for arq in arqvs:
        f = open(pasta+'/tokens/'+arq)
        words = f.read().splitlines()
        #words = ' '.join(words)
        docs.append(words)
        f.close()
    return docs


def lda_flavio(num_topics=10,pasta='./'):
    vocab = vocabulario(pasta)
    docset = documentos(pasta)
    
    K=num_topics
    D = len(docset) #Number of documents in the docset
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024, 0.7)
    i = 0
    for doc in docset:
        t1 = datetime.datetime.now()
        i += 1
        print 'Analistando documento %d de %d.' % (i, D)
        gamma, bound = olda.update_lambda(doc)
        wordids, wordcts = onlineldavb.parse_doc_list(doc,olda._vocab)
        perwordbound = bound * len(docset) / (D*sum(map(sum,wordcts)))
        delta_t = datetime.datetime.now()-t1
        print 'Documento  %d de %d em %d segundos.'%(i, D, delta_t.seconds) #2134 segundos ~ 35 min.

    np.savetxt(pasta+'lda_lambda.txt',olda._lambda)
    print 'Fim do LDA'
    return vocab, olda._lambda


def lda_gensim(pasta, num_topics):
    texts = documentos(pasta)
    
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=num_topics)
    
    lda.save(pasta+'/lda')
    dictionary.save(pasta+'/dic')
    dictionary.save_as_text(pasta+'/dic.txt')  
    
    
    return (dictionary,corpus,lda)

def gensim_extract(lda, n_topics=10, n_words=10):
    p = []
    for top in lda.show_topics(topics=n_topics, topn=n_words):
        lista_p = top.split(' + ') 
        vk = [(l.split('*')[1],float(l.split('*')[0])) for l in lista_p ]
        p.append(vk)
        #[l[1] for l in lista_v]
    return p



def gera_wordclouds(lda, pasta='./', n_topics=10, n_words=10):
    i = 0
    html = '<html><body>\n'
    
    for topico in gensim_extract(lda, n_topics=n_topics, n_words=n_words):
        i += 1
        words = []
        prob = []
        for item in topico:
            words.append(item[0])
            prob.append(item[1])
        topics.append(words)
        img = 'topico_{:02}.png'.format(i)
        make_wordcloud(np.array(words), np.array(prob), fname="{}/{}".format(pasta, img), font_path=FONT_PATH, width=600, height=300)    
        html += '<div><img src="'+img+'" style="margin:10px"/></div>\n'

    html += '</body></html>'

    fname = pasta+'/topicos.html'
  
    f = open(fname, 'w')
    f.write(html)
    f.close()

def obtem_topicos(lda, pasta='./', n_topics=10, n_words=10):
    topics = []
    dist = []
    for t in gensim_extract(lda, n_topics=n_topics, n_words=n_words):
        words = []
        prob = []
        for item in t:
            words.append(item[0])
            prob.append(item[1])
        topics.append(words)
        dist.append(prob)
    return topics,dist

    
def exibe_wordclouds_inline(pasta='.'):
    for img in glob.glob(pasta+'/*.png'):
        display(Image(filename=img))
