## Fundação Getúlio Vargas

## Modelagem de Assuntos

Profº Flavio 

Aluno: Sérgio da Silva Rodrigues

===

#### Introdução
Este trabalho apresenta uma aplicação do modelo estatístico [Latent Dirichilet Algorithm](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation), LDA, tomando-se como [corpus](http://en.wikipedia.org/wiki/Text_corpus) as obras de  [Machado de Assis](http://pt.wikipedia.org/wiki/Machado_de_Assis). 

![LDA nas obras de Machado de Assis](/assets/lda_intro.png "LDA nas obras de Machado de Assis")

A motivação para esta escolha de corpus foi o interesse em avaliar o comportamento do LDA em obras literárias, documentos com extenso vocabulário, e provavelmente um grande número de tópicos utilizados seguindo o modelo gerador do LDA. A escolha das obras de Machado de Assis deve-se pela disponibilidade de seus textos já estruturados para processamento na biblioteca [NLTK](http://nltk.org). Consequentemente utilizamos [Python](http://python.org) como linguagem de suporte à análise, e a implementação Python do LDA  selecionado é a biblioteca  [GENSIM](http://radimrehurek.com/gensim/). 


#### Ferramentas utilizadas

[Python 2.7](http://www.python.org) - linguagem de programação para automação o modelo.

Bilbioteca [NLTK](http://nltk.org) - corpus estruturado do escritor Machado de Assis. 

Biblioteca [GENSIM](http://radimrehurek.com/gensim/) - implementação do algoritmo LDA.

#### Pré processamento do corpus
O corpus das obras do escritor Machado de Assis estruturado na biblioteca NLTK contém uma coleção de 137 contos, 45 críticas literárias, 24 crônicas, 7 poesias, 10 peças de teatro, 10 miscelâneas, 3 traduções e 10 romances, totalizando 246 documentos.
A primeira etapa do trabalho consiste em remover dos documentos palavras indesejadas, de pouco valor semântico ao objetivo da modelage, tais como preposições e artigos, conhecidas como [*stop words*](http://en.wikipedia.org/wiki/Stop_words). Em um primeiro momento, utilizamos os stop words disponívies na função `stopwords(language)` do NLTK.  
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


Finalmente, podemos executar o LDA, chamando a função `ldamodel.LdaModel()` passando o corpus, o dicionário e número de tópicos a ser encontrado.
    
    lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=num_topics )

Neste código, corpus é o `bag-of-words` construído na etapa anterior, o parâmetro `id2word` recebe o próprio dicionário, para que ao imprimir os resultados o texto contenha as palavras ao invés dos identificadores, e `num_topics` é o número de tópicos a ser analisado, uma restrição do algorimto LDA e que na biblioteca GENSIM possui o valor default de 10.

Após o processamento, para visualizar o resultado chamados a função `lda.show_topics()`, cuja saída é:

    ['0.050*cabe\xc3\xa7a + 0.034*helena + 0.026*palavra + 0.025*gilliatt + 0.013*em\xc3\xadlia + 0.013*cec\xc3\xadlia + 0.010*costa + 0.009*lethierry + 0.008*leonor + 0.008*tito',
     '0.038*casa + 0.033*tempo + 0.032*olhos + 0.031*homem + 0.029*coisa + 0.024*dois + 0.022*duas + 0.022*dizer + 0.022*havia + 0.021*todos',
     '0.033*pedro + 0.028*mesma + 0.023*senhor + 0.020*oliver + 0.018*janela + 0.016*estela + 0.014*grande + 0.013*comigo + 0.012*muita + 0.012*digo',
     '0.030*nome + 0.030*quatro + 0.024*gilliatt + 0.018*mesa + 0.017*pequeno + 0.015*rubi\xc3\xa3o + 0.015*valentim + 0.014*\xc3\xa1gua + 0.014*jos\xc3\xa9 + 0.013*elisa',
     '0.019*\xc3\xa1gua + 0.018*gilliatt + 0.018*vento + 0.017*livro + 0.015*alves + 0.011*padre + 0.009*paulo + 0.008*navio + 0.008*flor + 0.008*cam\xc3\xb5es',
     '0.068*senhora + 0.050*lu\xc3\xads + 0.034*carlota + 0.030*oliver + 0.030*senhor + 0.027*gente + 0.021*pessoa + 0.020*desde + 0.016*cabe\xc3\xa7a + 0.015*horas',
     '0.031*judeu + 0.023*raz\xc3\xa3o + 0.022*jorge + 0.022*quer + 0.021*modo + 0.021*devia + 0.020*ponto + 0.020*nenhuma + 0.017*nenhum + 0.017*mundo',
     '0.032*lado + 0.024*preciso + 0.023*sabe + 0.021*sala + 0.021*primeira + 0.019*terra + 0.019*lugar + 0.018*parte + 0.017*parece + 0.015*quero',
     '0.046*bar\xc3\xa3o + 0.046*cena + 0.037*dumont + 0.032*joana + 0.027*mathilde + 0.026*alvarez + 0.023*rosinha + 0.021*durval + 0.019*tito + 0.018*larcey',
     '0.013*respondeu + 0.011*parecia + 0.007*pobre + 0.007*continuou + 0.007*entrou + 0.007*ficou + 0.006*fazia + 0.006*queria + 0.006*crian\xc3\xa7a + 0.006*velha']

Cada linha do vetor é um tópico, e seu conteúdo representa palavras mais relevantes e suas respectivas distribuições. Como o formato não é nada agradável à leitura, construímos um extrator, `topicos_txt`, para visualizar as palavras em forma de coluna. Temos então a seguinte tabela para 10 tópicos e 20 palavras mais relevantes:
    
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

Nota-se a repetição de muitas palavras entre os tópicos, o que nos leva a crer que o modelo não está sendo corretamente utilizado, e de fato não está, pois ao passar todo o corpus de uma única vez para o LDA o mesmo teve como resultado uma distribuição quase uniforme entre as palavras. Alteramos o código para processar os documentos do corpus iterativamente, um documento por vez, permitindo que a distribuição  posterior fosse atualizada em cada iteração.

    texts = documentos(pasta,filtro)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = ldamodel.LdaModel([corpus[0]], id2word=dictionary, num_topics=num_topics )
    for i in range(1,len(corpus)):
        lda.update([corpus[i]])

    
Após a execução do modelo, o resultado encontrado é mais expressivo que o anterior:    

    +------------+--------+---------+-----------+------------+------------+---------+----------+-----------+-----------+
    |   Topic0   | Topic1 |  Topic2 |   Topic3  |   Topic4   |   Topic5   |  Topic6 |  Topic7  |   Topic8  |   Topic9  |
    +------------+--------+---------+-----------+------------+------------+---------+----------+-----------+-----------+
    |   cabeça   |  casa  |  pedro  |    nome   |    água    |  senhora   |  judeu  |   lado   |   barão   | respondeu |
    |   helena   | tempo  |  mesma  |   quatro  |  gilliatt  |    luís    |  razão  | preciso  |    cena   |  parecia  |
    |  palavra   | olhos  |  senhor |  gilliatt |   vento    |  carlota   |  jorge  |   sabe   |   dumont  |   pobre   |
    |  gilliatt  | homem  |  oliver |    mesa   |   livro    |   oliver   |   quer  |   sala   |   joana   | continuou |
    |   emília   | coisa  |  janela |  pequeno  |   alves    |   senhor   |   modo  | primeira |  mathilde |   entrou  |
    |  cecília   |  dois  |  estela |   rubião  |   padre    |   gente    |  devia  |  terra   |  alvarez  |   ficou   |
    |   costa    |  duas  |  grande |  valentim |   paulo    |   pessoa   |  ponto  |  lugar   |  rosinha  |   fazia   |
    | lethierry  | dizer  |  comigo |    água   |   navio    |   desde    | nenhuma |  parte   |   durval  |   queria  |
    |   leonor   | havia  |  muita  |    josé   |    flor    |   cabeça   |  nenhum |  parece  |    tito   |  criança  |
    |    tito    | todos  |   digo  |   elisa   |   camões   |   horas    |  mundo  |  quero   |   larcey  |   velha   |
    |  coronel   | podia  |  cinco  |   oliver  |   sombra   | cavalcante | ocasião | vontade  | esperança |   oliver  |
    |   irmão    | noite  |  outras |   senhor  | lethierry  |   doutor   | próprio | espírito |   flores  |  ninguém  |
    |   causa    |  pode  |  idéias |    deus   |   fundo    |   sikes    |  clara  |  creio   | margarida |    medo   |
    | impossível | alguma | pessoas |   sofia   |   rosto    |  baronesa  |   quis  | gilliatt |   leonor  |   horas   |
    |  silêncio  |  vida  |  creio  | lethierry |   manuel   |  palavra   | caminho | simples  |   emília  |   homens  |
    |  momento   | porta  |  falar  |   contra  |    doce    |   bumble   |  neste  |  nesse   |  martins  |   muitas  |
    |   clubin   | alguns |  pessoa |   mundo   |   clubin   |   cidade   |  deste  | daquela  |  tristão  |   ouviu   |
    | déruchette | grande |  sikes  |   clubin  |    cima    |  leocádia  |  maior  |   alto   |    povo   |  minutos  |
    |   sonho    | fazer  |  amigos |  júpiter  | déruchette |   dumont   |  oliver |  porém   |  fidélia  |    saiu   |
    |  durande   |  dias  |  chapéu |  pinheiro |  durande   |   mulher   |   hora  |  contra  |   terra   |   voltou  |
    +------------+--------+---------+-----------+------------+------------+---------+----------+-----------+-----------+

Agora podemos perceber a ocorrência de palavras únicas em alguns tópicos, mas ainda não é possível discernir uma diferenciação significativa entre eles. De fato, analisamos toda a obra de Machado de Assis, romances, crônicas, contos, críticas e miscelânea. Talvez seja mais apropriado analisar cada tipo de obra. Romances, por exemplo, são textos longos, onde há uma grande repetição de verbos, afinal, os personagens executam ações para que a história desenvolva. Será correto esperar que os verbos tenham uma probabilidade nos tópicos maior que os substantivos, ou os próprios personagens? Vejamos o resultado do LDA aplicado somente aos romances: 
	
	+-------------+--------------+----------+---------+---------+-------------+---------+----------+-------------+---------------+
	|    Topic0   |    Topic1    |  Topic2  |  Topic3 |  Topic4 |    Topic5   |  Topic6 |  Topic7  |    Topic8   |     Topic9    |
	+-------------+--------------+----------+---------+---------+-------------+---------+----------+-------------+---------------+
	|     casa    |    capitu    |  rubião  |   casa  |  olhos  |    gente    |  gosto  |  gente   |    rubião   |     paulo     |
	|    rubião   |    padre     |  tempo   |   dias  |  tempo  |    flora    |   pois  |   ouvi   |     casa    |     tempo     |
	|   assunto   |     josé     |   dois   |  coisa  |  grande |    aires    |  pessoa | grandes  |    sofia    |     flora     |
	|    volta    |   escobar    |  olhos   |   dois  |   casa  |     dois    |   digo  |  velho   |   tristão   |     aires     |
	|     dois    |     acho     |   casa   |  viúva  |  coisa  |     casa    |   três  |   boca   |    marido   |      rita     |
	|    embora   |    comigo    |  dizer   |  dizer  |   ouvi  |    tempo    |   tais  |  muitas  |   fidélia   | desembargador |
	|    marido   |  seminário   |  podia   |  alguma |  gente  |    pedro    |   nome  | saudades |   flamengo  |     pedro     |
	|    olhos    |   tristão    |  mesma   |  filho  |  outros |    olhos    | memória |  ofício  |    aguiar   |    depressa   |
	|     quis    |   fidélia    |   duas   |   duas  |  dizer  |    velha    |  terra  |   pena   |    olhos    |   natividade  |
	|   tristão   |     casa     |  santa   |   pode  |   vida  |     quis    |   cada  |   cara   |    maria    |    costume    |
	|   fidélia   |    aguiar    |  coisa   |  creio  |   dois  |   política  |  muita  |  prazer  |    carmo    |     olhos     |
	| conselheiro | naturalmente |  apesar  | tristão |  todos  |   pessoas   |  saber  |  outros  |    coisa    |     cartas    |
	|    amigo    |    missa     |  passar  | fidélia | verdade |  natividade |  quatro |  amigos  |    podia    |      dois     |
	|    poucos   |    carmo     |  viúva   |  mesma  |   dias  |     pode    |  fazia  |  praia   |    dizer    |      moça     |
	|    amigos   |    glória    |   alma   |  coisas |   pode  | conversação |  acabou |  olhos   | conversação |      dias     |
	|    capaz    |   bentinho   | costume  | verdade | pessoas | conselheiro |  homens |   cima   |    palha    |     santa     |
	|    tempo    |    falou     |  noite   |  tempo  |  melhor |    estar    |  maior  |   fica   |    banco    |    segunda    |
	|    gente    |    europa    | começou  |  grande |  mesma  |   palavras  |  papel  |  vieram  |    tempo    |     santos    |
	|     pode    |   justina    |  pediu   |  podia  |  alguma |    amigos   | própria |  contou  |     duas    |    coração    |
	|    carta    |    cosme     | depressa |  marido |   anos  |    irmão    |  comigo |  cidade  |     pode    |     filhos    |
	+-------------+--------------+----------+---------+---------+-------------+---------+----------+-------------+---------------+

Esse corpus possui os 10 romances de Machado de Assis, então escolhemos 10 tópicos como entrada para o LDA. Diferente do que esperávamos, os verbos não são as palavras mais relevantes dos tópicos. Podíamos esperar também que os personagens ficassem localizados em tópicos exclusivos, mas esse não foi o caso de Rubião, personagem do romance [Quincas Borba](http://pt.wikipedia.org/wiki/Quincas_Borba), uma das três obras que compõe a [trilogia realista](http://pt.wikipedia.org/wiki/Trilogia_Realista).  Tristão, personagem do romance [Memorial de Aires](http://www.sosestudante.com/resumos-m/memorial-de-aires-machado-de-assis-2--2.html) aparece ainda em mais tópicos do que Rubião. Uma análise qualitativa do resultado do LDA com este corpus requer conhecimento da obra de Machado de Assis, o que está além do alcance deste trabalho. Mas podemos perceber que talvez o LDA não seja apropriado para classificação de obras literárias, sendo cada obra um documento para o modelo. Podemos propor como trabalho futuro a análise individual das obras, tomando-se os capítulos como documentos, a fim de determinar os tópicos presentes a cada capítulo, e talvez explicitar uma evolução  dos tópicos relevantes conforme a cronologia da obra.

Tentemos então analisar a coleção de contos, textos mais curtos, seguindo a idéia proposta acima, mantendo o número de tópicos em 20, e exibindo as 20 palavras mais relevantes.

	+------------+------------+-------------+-----------+-----------+-------------+-------------+-----------+------------+------------+-----------+------------+-------------+------------+-----------+-----------+-----------+------------+-----------+-------------+
	|   Topic0   |   Topic1   |    Topic2   |   Topic3  |   Topic4  |    Topic5   |    Topic6   |   Topic7  |   Topic8   |   Topic9   |  Topic10  |  Topic11   |   Topic12   |  Topic13   |  Topic14  |  Topic15  |  Topic16  |  Topic17   |  Topic18  |   Topic19   |
	+------------+------------+-------------+-----------+-----------+-------------+-------------+-----------+------------+------------+-----------+------------+-------------+------------+-----------+-----------+-----------+------------+-----------+-------------+
	|   contos   |   camilo   |    irmão    |  henrique |  oliveira |     flor    |    xavier   |   marido  |  escrivão  | fernandes  |   tomás   |   paulo    |    julião   |  coimbra   |    irmã   |   olhos   |  barreto  |   versos   |   camila  |  henriqueta |
	|  ricardo   |   cobra    |   joaninha  |  bagatela |  genoveva |   martinha  |     góis    |   amiga   |   grande   |   estela   |   raquel  |    cruz    |   pimentel  |   máximo   |  jucunda  |   tempo   | ermelinda |   morrer   |   paula   |     casa    |
	|  marcela   |   bicho    |    julião   |  ventura  |  carlota  |   porfírio  |     dona    | gonçalves |   estela   |   tomás    |   matias  |  cardeal   | fernandinha |  loteria   |  oficial  |    dias   |   baile   |   janela   |  artista  |     moça    |
	|  coimbra   |    leão    |  inglesinha |   morto   |   sonho   |    glória   |     nohr    |  genoveva |   sótão    |   raquel   | severiano |  general   |   palavra   |  bilhete   |  madrinha |    dois   |  brandão  |  alberta   |  valentim |    julião   |
	| felismina  | almanaques |   barcelos  |   quatro  |   tomás   |   vestido   |    rosas    |   vieira  |  castelo   |   sótão    |   clara   |    josé    |    sales    |   escola   |  raimunda |    anos   |  cesário  |   finoca   |   vênus   |   pimentel  |
	|  romualdo  | esperança  |    caldas   |    nohr   |   raquel  |   ezequiel  |   charmion  |   xavier  |  coimbra   |  castelo   |  barreto  |  julieta   |    rindo    | quinhentos |   carmo   |   coisa   |    bota   |   macedo   |  clarinha | fernandinha |
	|  loteria   |   tobias   | fernandinha |   tomás   | marcelina |    neves    |  jardineiro |  jucunda  |   mesma    |  malvina   |  romualdo |  marques   |    cabeça   |   sorte    |   teatro  |    vida   |  direita  |   estela   |  ernesto  |     dois    |
	|   escola   | bonifácio  |   cecília   |   raquel  |  beatriz  | consciência |   escriba   |  alberta  |    nohr    |   mesma    |  delfina  |   seixas   |  legazinha  |  bernardo  |    quis   |  família  |  esquerda |   sótão    |   xavier  |    estela   |
	|  bilhete   |  eulália   |  celestina  |  charmion | professor |   delgado   |    egito    |   finoca  |  loteria   |   duarte   | ermelinda |  leocádia  |    tomás    | irmandade  |  eusébio  |   alguns  |  eduardo  |  castelo   |   teatro  |   família   |
	| quinhentos |   gomes    |   palavra   |  escriba  |  eduardo  |    bento    |    faraó    |    góis   |  bilhete   |  barreto   |   baile   |  augusto   |    raquel   |   teatro   |   cirila  | perguntou |   botas   |  ricardo   |    quis   |   palavra   |
	|   sorte    |  gustavo   |    rindo    |   egito   | bastinhos |   cândido   |    mucama   |   macedo  |   escola   |  família   | fernandes | madureira  |    quadro   |    quis    |  dolores  |    casa   |   pedro   |   mesma    |  bagatela |     amor    |
	|  bernardo  |    fita    |    cabeça   |   faraó   |   laura   |   capitão   |   barbosa   |  valentim | quinhentos | ermelinda  |   xavier  |   elvira   |    jantar   |   pobre    |  anacleto |  coração  |    lulu   |  andrade   |  ricardo  |    caldas   |
	| irmandade  |   máximo   |   pimentel  |   luísa   |  anacleto |   anacleto  |    joana    |    dona   |  bernardo  |   baile    |  alberta  |  germano   |   julieta   |  bagatela  |  adriano  |   porta   |  emiliana |  bagatela  |    góis   |    rindo    |
	|  carteira  | procurador |    romeu    |  rochinha |  adriano  |   adriano   |    inácio   |   sonho   |   sorte    |   grande   |   finoca  |  cândido   |   augusto   |    cruz    |  fagundes |   melhor  | alexandre |  marcela   |  ventura  |    cabeça   |
	|  honório   | colchoeiro |    major    | professor |   caldas  |    inácia   |  violoncelo |    irmã   | irmandade  |  romualdo  |  antunes  | colchoeiro |  bastinhos  |  cardeal   |  monteiro |    duas   |   ambas   |  família   |    dona   |    sótão    |
	| fernandes  |   pálida   |   bacharel  |   vieira  |  fagundes |   fagundes  |   machete   |  madrinha |  charmion  |  programa  |   macedo  |   rufina   |   leocádia  |  general   |   desde   |    réis   |   miloca  | felismina  |   morto   |   joaninha  |
	|  escrivão  |   rufina   |    emílio   |   toledo  |  pimentel |  damasceno  |    amaral   |  raimunda |  família   |  ministro  |  programa |   ângela   |    todas    |  ventura   | boticário |   viúva   |   adolfo  |   grande   |  marcela  |   castelo   |
	|   corte    | marianinha |   venância  |   amiga   |  monteiro |   monteiro  |    júlio    |  ernesto  |  escriba   |   mestre   |    góis   |  alfredo   |     lata    |   morto    |  madalena |   sobre   |  vocação  | henriqueta | felismina |    tempo    |
	|  programa  |   pobre    |    marcos   |  cândido  |   desde   |   barbeiro  | instrumento |   carmo   |   egito    |   vizir    |  ministro |   inácia   |    estilo   |   josefa   |   vinte   |   velho   |  rodrigo  |  ventura   |   prima   |    mesma    |
	|  ministro  | estudante  |   eugênia   |   europa  | boticário |    votos    |    cartas   |  rochinha |   faraó    | escritório |    dona   |  valério   |     rabo    |  mariana   |   pinto   |   jantar  | pulquéria |   morto    |  henrique |   ricardo   |
	+------------+------------+-------------+-----------+-----------+-------------+-------------+-----------+------------+------------+-----------+------------+-------------+------------+-----------+-----------+-----------+------------+-----------+-------------+

Ainda assim, notamos que os nomes dos personagens ocorrem em mais de um tópico, e entre as 20 palavras mais relevantes não há substantivos sufucientes para um discernimento apropriado entre os tópicos.
 
Sendo uma avaliação qualitativa literária fora do escopo deste trabalho, decidimos usar um corpus mais adequado a este tipo de análise, e recorremos novamente ao [NLTK](http://nltk.org), usando o dataset [Mac Morpho](http://www.nilc.icmc.usp.br/lacioweb/corpora.htm), uma coletânea de artigos dos cadernos de Esportes, Dinheiro, Ciência, Agronomia, Informática, Mundo, Brasil e Cotidiano, do jornal [Folha de São Paulo](http://www.folha.uol.com.br), restritos ao ano de 1994.

Eis o resultado com 10 tópicos e 20 palavras.

    +---------------+------------+----------------+------------------+---------------+---------------+-------------+------------+-------------+------------------+
    |     Topic0    |   Topic1   |     Topic2     |      Topic3      |     Topic4    |     Topic5    |    Topic6   |   Topic7   |    Topic8   |      Topic9      |
    +---------------+------------+----------------+------------------+---------------+---------------+-------------+------------+-------------+------------------+
    |     premiê    |   poesia   |     poeta      |     sérvios      |     mais!     |     duran     |     6-13    |   página   |   cubanos   |      trakl       |
    |  protestantes |   poemas   |    benetton    |    muçulmanos    |     balsa     |    fujimori   |     6-14    |  editoria  |   irlandês  |       balé       |
    |   palestinos  |    tel.    |   veteranos    |       2-10       |      gene     |    racismo    |    still    |   sobre    |    poema    |    balanchine    |
    |      2-10     |   freud    |     perdi      |     sarajevo     |     raoul     |     freud     |   paisagem  |    anos    |    milão    |    albaneses     |
    |    ieltsin    |  benjamin  |   balanchine   |     expulsa      |  nacionalista |   whitewater  |  geometria  |   mundo    |  escritores |      freud       |
    |     arafat    |   rocco    |   cunningham   |      caças       |    science    |     nudez     |     tel.    |  governo   |    poeta    | homossexualidade |
    |    belfast    | balanchine |   monarquia    |      mais!       |    colorado   |      tel.     | ilustrações |    país    |  espetáculo |     salinas      |
    |   libertação  |  aguilar   |   despertou    |     religião     |  nacionalismo |   biografia   |  mensagens  |    dois    |    mais!    |      poetas      |
    |      otan     |    6-13    |     raiva      |     perpétua     |      tel.     |   católicos   |   infinito  | presidente |   chicago   |    cingapura     |
    |      fein     | histórias  |      tel.      |  manifestantes   | originalidade |     morrem    |    terror   |  segundo   |    george   |      graham      |
    |      sinn     |    6-14    |    talento     |       papa       |   escritora   |     bronx     |   sombras   |  pessoas   |  cunningham |   modernidade    |
    |   católicos   |  queimar   |      gaza      |     croatas      |    estonia    | contemporânea |   espiral   |   contra   |    russos   |      georg       |
    |    chiapas    |  estonia   |  objetividade  |      haiti       |     ascher    |    galáxia    |  balanchine |    pode    |   triunfo   |       otan       |
    |    caldera    |  poética   |  observações   |     islâmico     |     rocco     |      gaza     |    micros   |   brasil   |    araras   |     nazista      |
    |     hamas     |  crônicas  |  maravilhoso   | fundamentalistas |    colosio    |    derruba    |  satélites  |   livro    |     ódio    |       6-11       |
    |  israelenses  |   press    |   williamson   |       lage       |   proteínas   |   invisíveis  |  astronomia |   outros   |   comecei   |      navio       |
    |      ruiz     | filósofos  |   incomodar    |     rejeitam     |   criticaram  |      6-10     |   desejar   |    nova    | coreografia |       mama       |
    |   israelense  |   raros    |      copo      |       f-16       |     arena     |    belfast    |    laços    |   paulo    |  bailarinos |      martha      |
    |      papa     |    6-16    | impressionante |      sérvia      |   britânicos  |     boris     |    célula   |    três    |    treino   |    literário     |
    | primeira-dama |  paradoxo  |      lyon      |  sequestradores  |     1.250     |    airlines   |     6-10    |   desde    |    berlim   |   terroristas    |
    +---------------+------------+----------------+------------------+---------------+---------------+-------------+------------+-------------+------------------+


Aqui já podemos notar que as palavras mais relevantes criam um contexto diferenciado entre os tópicos. Por exemplo, o "Topic0" relacina-se ao Oriente Médio, "Topic1" à literatura, "Topic2" política internacional, mas sensivelmente diferente de "Topic0", etc. 

Aumentando o número de tópicos, esperamos que as palavras mais relevantes possam apresentar um contexto melhor. Vejamos o que acontece com 20 tópicos.
	
	+------------+--------------+-----------------+--------------+------------------+-------------+-------------+--------------+--------------+---------------+--------------+-------------+-------------+---------------+-------------------+--------------+---------------+---------------+----------------+------------+
	|   Topic0   |    Topic1    |      Topic2     |    Topic3    |      Topic4      |    Topic5   |    Topic6   |    Topic7    |    Topic8    |     Topic9    |   Topic10    |   Topic11   |   Topic12   |    Topic13    |      Topic14      |   Topic15    |    Topic16    |    Topic17    |    Topic18     |  Topic19   |
	+------------+--------------+-----------------+--------------+------------------+-------------+-------------+--------------+--------------+---------------+--------------+-------------+-------------+---------------+-------------------+--------------+---------------+---------------+----------------+------------+
	|   página   |    premiê    | norte-americana |    poesia    |      mais!       |   perpétua  |     otan    |    terror    |    avião     |    ieltsin    |     ruiz     |    poeta    |  espanhóis  |     mais!     |      fujimori     |   cubanos    |     balsa     |    reynolds   |   católicos    |  tradução  |
	|  editoria  |   sérvios    |      milão      |    poemas    |     expulsa      | protestante |  palestina  |    tropas    |     papa     |     bósnia    |   chiapas    |    berlim   |  orgulhoso  |      ódio     | primeiro-ministro |    poema     |   britânicos  |      tel.     |     duran      |   mestre   |
	|   sobre    |     2-10     |     sombras     |   american   |      caças       |    adams    |  refugiados |    nixon     |    bomba     | primeira-dama |   zedillo    |   explodiu  |  interessar |    jandira    |        otan       |    russos    |     raoul     |     rocco     |   prometido    |  clareza   |
	|    anos    |  muçulmanos  |     triunfo     |     6-13     |       lage       | modernidade |     fein    |  chanceler   |   ensaios    |    intenção   |   sérvios    |   irlandês  |     leon    |    buchada    |        balé       |   irlandês   |    erotismo   |    benjamin   |  sentimentos   | incomodar  |
	|   mundo    |   caldera    |    franceses    |    street    |    atmosfera     |    ballet   |     sinn    |    golfo     |   chinesa    |   whitewater  |  ex-premiê   |    dublin   |  antologia  |    religião   |       trakl       |  escritores  |  nacionalismo |    filósofo   |    orgulho     |  músicos   |
	|  governo   |  palestinos  |      luigi      |     6-14     |     sarajevo     |    georg    |   secreto   |   science    |   humanas    |     egito     |   colosio    |    helmut   |  montanhas  |    rejeitam   |       freud       |   benetton   |  nacionalista |     fóssil    |     susto      |  poderoso  |
	|    país    |   hillary    |    espetáculo   |   paisagem   |      líbano      |   bolívar   |  livrarias  |   cúmplice   |  concepção   |    heroína    | documentário |   benetton  |  moralmente |   guarnieri   |     albaneses     |   chicago    |     arena     |     idioma    |    encarar     | emocional  |
	|    dois    |   belfast    |      vidas      |    aliada    |      argel       |    lorena   |   fujimori  |    rubio     |    atores    |    racismo    |  jirinovski  |  cunningham |    diabos   |      rasi     |     cingapura     |   sensação   |    gangues    |    modesto    |  republicano   |  cansado   |
	| presidente |  israelense  |     basquete    | especulações |      sérvia      |  dramático  | terroristas |    laços     |  culturais   |  protestantes |   estonia    |    perdi    |   protetor  | gianfrancesco |       poetas      |   nápoles    |     drama     |     ascher    |   fidelidade   |   esfera   |
	|  segundo   | israelenses  |     negociam    |   derruba    |   terroristas    |    atacam   |  palestinos |   colorado   |     1974     |     warren    |    louis     |    raiva    | coreografia |    instante   |       judeu       |   charles    | originalidade |   filósofos   |   indicações   |   freud    |
	|  pessoas   | protestantes |    lentamente   |  partículas  |     haroldo      | terroristas |   cruzando  |     2-10     |  incidentes  |     jericó    |   príncipe   |     lyon    |    deuses   |     babel     |      paradoxo     |    árabes    |   cavalcanti  |    mutações   |    desperta    |   músico   |
	|   contra   |    arafat    |      luzes      |    still     |    violações     |     2-10    |  jirinovski |    press     | protestantes |   palestinos  |    arafat    |  represália |  dinamarca  |   históricas  |    coreografia    |    disco     |   universais  |    ocidente   |    decretar    |   pequim   |
	|    pode    |   sarajevo   |      viaja      |   jornada    |      freud       |   bobbitt   |  imaginação |  histórias   |  criminosos  |  compreender  |    crânio    | protestaram |    martin   |     exato     |      salinas      |    grego     |   escritora   |    poética    |   atualidade   |   viana    |
	|   brasil   |    cedras    |    distantes    | ilustrações  |      sérvio      |   destrói   |     2-10    |  poderosos   |    vidro     |   católicos   |     1912     |   expulsos  |    stern    |   muçulmana   |      balladur     |    george    |   espectador  | nacionalistas | sequestradores | balanchine |
	|   livro    |    iasser    |   criatividade  |  multimídia  |     sérvios      |  bailarinos |     kohl    |   cristãos   |  obrigados   |    convida    |   gortari    |    araras   |  destruído  |    islâmico   |      galáxia      |  iugoslávia  |      1948     |  psicanalista |    estende     |   versos   |
	|   outros   |  embaixada   |     vencidos    |   infinito   |     islâmico     |    trisha   |    premiê   | protestantes |     2-10     |     míssil    |    reabre    |     lema    |   realista  |     plínio    |       imago       |    amante    |   religiosos  |  científicas  |    ousadia     | neurônios  |
	|    nova    |  atentados   |    extermínio   |    cd-rom    | fundamentalistas |  celebrada  |    teerã    |  ancestrais  |  violentos   |    escravos   |  palestinos  |     1971    |     1953    |    tornado    |      airlines     | sul-africano |   encenação   |    sectária   |     exibe      |  prefiro   |
	|   paulo    |  católicos   |     fazerem     |  reabertura  |      carter      |   salinas   |    herald   |    poemas    |  assistiram  |     autora    |    perry     |    esboço   |    ombros   |     pietro    |     catástrofe    |    treino    |    leituras   |    fósseis    |   semanário    |   tribo    |
	|    três    |    matam     |     abstrato    |  distinção   |      carlo       |  balanchine |    arafat   |    bruxas    |    louco     |     latino    |  pentágono   |   talento   |   peculiar  |     london    |     artilharia    |    menem     |     convém    |     france    |      camp      |  aprendeu  |
	|   desde    |     kohl     |     secreta     |   formato    |      bósnio      |  dançarinos |   belfast   |  proteínas   |  enterrado   | contemporânea | narcotráfico |  disparado  |    morris   |   elegância   |      romances     |  britânicos  |   traduções   |      sons     |     farsa      |  gráfico   |
	+------------+--------------+-----------------+--------------+------------------+-------------+-------------+--------------+--------------+---------------+--------------+-------------+-------------+---------------+-------------------+--------------+---------------+---------------+----------------+------------+