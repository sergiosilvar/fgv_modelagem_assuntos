## Fundação Getúlio Vargas

## Modelagem de Assuntos

Profº Flavio 

Aluno: Sérgio da Silva Rodrigues

===

#### Objetivo
Modelagem de Assuntos utilizando o [Latent Dirichilet Algorithm.](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CCsQFjAA&url=http%3A%2F%2Fen.wikipedia.org%2Fwiki%2FLatent_Dirichlet_allocation&ei=kfNrU-OLINGxsASj0IDwCQ&usg=AFQjCNFbSU0wf-VjgZqlUY_lMnUjO9BTKA&sig2=OFtPmzdqWQEig8anEYxzKw&bvm=bv.66111022,d.cWc)

#### Dataset 
Obras literárias de [Machado de Assis](http://pt.wikipedia.org/wiki/Machado_de_Assis), obtidas da biblioteca NLTK.

#### Ferramentas utilizadas

[Python 2.7](http://www.python.org)

Bilbioteca [NLTK](http://nltk.org)

Biblioteca [GENSIM](http://radimrehurek.com/gensim/)

#### Descrição
O corpus das obras do escritor Machado de Assis contém uma coleção de 137 contos, 45 críticas literárias, 24 crônicas, 7 poesias, 10 peças de teatro, 10 miscelâneas, 3 traduções e 10 romances, totalizando 246 documentos. 
Os documentos foram pré processados para remover palavras indesejadas como preposições, interjeições e outras de pouco valor semântico ao interesse da análise. Estas palavras estão registradas no arquivo stopwords_pt.txt.
Após a removação das palavras comuns, cada documento foi tokenizado e [armazendo em arquivos](https://github.com/srodriguex/fgv_modelagem_assuntos/tree/master/machado/tokens) para otimizar futuras referências.

Para executar o LDA com o Gensim, ao contrário do que está [na documentação](http://radimrehurek.com/gensim/tut1.html#from-strings-to-vectors), primeiro é necessário construir a estrutura que representa o vocabulário a ser analisado, para após construir o [*bag-of-words*](http://en.wikipedia.org/wiki/Bag_of_words). Nessa primeira etapa, carregamos todo o corpus em memória, e o passamos como parâmetro do construtor da classe [Dictionary](http://radimrehurek.com/gensim/corpora/dictionary.html):

    texts = documentos(pasta)
    dictionary = corpora.Dictionary(texts)

A variável `pasta` indica a pasta raiz onde estão armazenados os documentos gerados no pré processamento. Dentro desta pasta há outra, chamada `tokens`, que contém os documentos tokenizados, um arquivo para cada documento. Esta foi uma decisão de projeto durante a construção iterativa do código para acelerar os testes, evitando o tempo necessário à tokenização e remoção das palavras indesejáveis.

A variável `dictionary` agora contém um identificador inteiro para cada palavra do corpus. Em seguida, construímos o *bag-of-words* iterando novamente em cada documento, só que agora utilizando o método `doc2bow`:

    corpus = [dictionary.doc2bow(text) for text in texts]

A saída deste método é um vetor de tuplas onde o primeiro elemento da tupla é o da palavra e o segundo elemento é a quantidade de ocorrências dessa palavra no documento. Então a variável `corpus` contém uma lista de lista de tuplas, onde cada elemento da primeira lista é uma lista de tuplas do respectivo documento analisado, por exemplo: 

    print corpus
    >> [[(0, 1), (1, 1), (2, 1)],
       [(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
       [(2, 1), (5, 1), (7, 1), (8, 1)],
       [(1, 1), (5, 2), (8, 1)],
       [(3, 1), (6, 1), (7, 1)]]


Finalmente, podemos executar o LDA. Em uma primeira abordagem, ingênua, passamos o corpus inteiro para o algortimo, de uma só vez:

    lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=num_topics )

Neste código, corpus é o `bag-of-words` construído na etapa anterior, o parâmetro `id2word` recebe o próprio dicionário, para que ao imprimir os resultados o texto contenha as palavras ao invés dos identificadores, e `num_topics` é o número de tópicos a ser analisado, uma restrição do algorimto LDA e que na biblioteca GENSIM possui o valor default de 10.

O resultado encontrado foi:
    
    +---------+---------+---------+--------+--------+--------+---------+---------+---------+---------+
    |  Topic0 |  Topic1 |  Topic2 | Topic3 | Topic4 | Topic5 |  Topic6 |  Topic7 |  Topic8 |  Topic9 |
    +---------+---------+---------+--------+--------+--------+---------+---------+---------+---------+
    |   casa  |  tempo  |   casa  |  casa  |  casa  | coisa  |   casa  |   casa  |   casa  |   casa  |
    |  olhos  |   tito  |  coisa  | tempo  | coisa  |  casa  |  tempo  |  olhos  |   dois  |  tempo  |
    |  homem  |   casa  |  tempo  | coisa  | tempo  | olhos  |  olhos  |  coisa  |  tempo  |  coisa  |
    |  tempo  |  coisa  |   vida  | olhos  |  dois  |  dois  |  homem  |  tempo  |  olhos  |   dois  |
    |   dois  |  olhos  |  olhos  | todos  | olhos  | tempo  |   dois  |  homem  |  coisa  |   moça  |
    |  coisa  |  todos  |  homem  | dizer  | todos  | poeta  |   amor  |   dois  |  homem  |  podia  |
    |  todos  |   dois  |   dois  |  duas  |  vida  | todos  |   moça  |   pode  |  todos  |  olhos  |
    |  dizer  |  dizer  |  dizer  | homem  | homem  | grande |   vida  |   dias  |   duas  |  homem  |
    |   vida  |  homem  |  todos  |  amor  | dizer  |  pode  |  coisa  |  todos  |   pode  |   vida  |
    |  senhor |   duas  |   duas  |  vida  |  dias  |  duas  |   pode  |  alguma |   moça  |   pode  |
    |   pode  |   anos  | coração |  pode  |  anos  | homem  |  poeta  |   vida  |   vida  |   amor  |
    |   amor  |  outros |   moça  | alguma |  moça  |  dias  | coração |   moça  |  mulher |   dias  |
    |  maria  |  alguns |  podia  |  dois  |  pode  | alguma |   duas  | coração |  grande |  dizer  |
    |  grande |  mulher |   pode  |  dias  |  duas  | dizer  |  noite  |  dizer  |   anos  |  alguns |
    |   dias  |   amor  |  alguns | alguns | alguns |  moça  |  pedro  |   anos  |  alguma |  alguma |
    |  alguma |  durval |  noite  |  luís  | alguma | alguns |  todos  |   amor  |  alguns |   anos  |
    |  outros | rosinha | verdade | podia  | grande |  anos  |  grande |  grande |   dias  |  senhor |
    |  noite  |  podia  |  alguma | grande | noite  | helena |  alguns |   duas  |  dizer  |  todos  |
    |  podia  |  fazer  |   anos  | fazer  |  toda  | sobre  |  alguma |  noite  | verdade |  carta  |
    | verdade |   vida  |  jorge  |  moça  | outros |  amor  |  dizer  |  outros | carlota | coração |
    +---------+---------+---------+--------+--------+--------+---------+---------+---------+---------+
, que *bag-of-words*,  repositório de palavras,

Devido a quantidade de documentos a processar, decidimos realizar um pré processamento 
dos documentos, removendo  foi utilizado o LDA da biblioteca GENSIM.
