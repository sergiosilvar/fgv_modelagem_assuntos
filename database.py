# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import json
import itertools

DIR = './json/'

def dominio():
    anos = [str(i) for i in range(2008,2014)]
    meses = ['%02d'%i for i in range(1,13)]
    result = list(itertools.product(anos,meses))
    dominio = [x+'-'+y for x,y in result]
    return dominio


def dataset(estado, cidade, bairro, num_quartos):
    fname = DIR+''+estado+'/'+cidade+'/'+bairro+'/%d_indices.json' % (num_quartos)
    f = open(fname,'r')
    ind = json.load(f)
    #ind = pd.io.json.read_json(fname)     
    f.close()
    return ind
    
def indices(estado=None, cidade=None, bairro=None, num_quartos=0):
    ds =  dataset(estado, cidade, bairro, num_quartos)[:(2013-2008+1)*12-1]
    lista  = [Indice(x) for x in ds]
    for ano_mes in dominio():
        tem = False
        for ind in lista:
            if ind.ano_mes == ano_mes:
                tem = True
                break
        if not tem:
            vazio = Indice()
            vazio.ano = int(ano_mes[:4])
            vazio.mes = int(ano_mes[-2:])
            lista.append(vazio)
    return sorted(lista, key=lambda indice: indice.ano_mes)

def lista_estados():
    return os.listdir(DIR)

def lista_cidades(estado=None):
    return os.listdir(DIR+'/'+estado)

def lista_bairros(estado,cidade):
    return os.listdir(DIR+'/'+estado+'/'+cidade)

class Zap(object):
    def __init__(self):
        pass
    
class Bairro(Zap):
    def __init__(self,estado,cidade,bairro):
        index_indice = 1
        index_mes = 0
        self.nome = bairro
        self.cidade = cidade
        self.estado = estado
        self.indices = [indices(estado,cidade,bairro,i)[index_indice] for i in range(4)]
        self.mes = indices(estado,cidade,bairro,0)[index_mes]
    
    def qt1(self):
        return self.indices[1]
    
    def qt2(self):
        return self.indices[2]
    
    def qt3(self):
        return self.indices[3]
    
    def qt0(self):
        return self.indices[0]
    
    def __repr__(self):
        return self.nome
    
class Cidade(Zap):
    def __init__(self, estado, cidade):
        self.nome = cidade
        self.estado = estado
        self.bairros = {}
    
    def lista_bairros(self):
        return lista_bairros(self.estado,self.nome)
    
    def bairro(self,nome_bairro):
        return self.bairros.get(nome_bairro,Bairro(self.estado,self.nome,nome_bairro))

class Indice(object):
    def __init__(self,json=None):
        if json != None:
            self.ano = json['Ano']
            self.valor = json['Valor']
            self.mes = json['Mes']
            self.var = json['Variacao']
            self.var_m = json['VariacaoMensal']
            self.amostras = json['Amostra']
            #self.ano_mes =  self._ano_mes
        else:
            self.ano = 0
            self.valor = 0
            self.mes = 0
            self.var = 0
            self.var_m = 0
            self.amostras = 0
            #self.ano_mes =  self._ano_mes
            
    @property
    def ano_mes(self):
        return '%d-%02d'%(self.ano, self.mes)
    
    def __repr__(self):
        return '%s: %f'%(self.ano_mes,self.valor)

# <codecell>


# <codecell>

%clear

# <codecell>

%clear

# <codecell>

%clear

