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

Alerta:

    2014-05-09 23:46:27,903 [MainThread  ] [WARNI]  too few updates, training might
    not converge; consider increasing the number of passes or iterations to improve
    accuracy

Após evolução:

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

Filmes:

    +------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    |   Topic0   |   Topic1   |   Topic2   |   Topic3   |   Topic4   |   Topic5   |   Topic6   |   Topic7   |   Topic8   |   Topic9   |
    +------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    |    film    |    film    |    film    |    film    |    film    |    film    |    film    |    film    |    film    |    film    |
    |    well    |    time    |    time    |   would    |    time    |    time    |   would    |    time    | characters | character  |
    |   films    |   people   | character  |    time    |   would    |   would    | characters |   would    |   would    |    time    |
    |    time    | characters |    well    | character  | characters | character  |    time    |    well    | character  |   really   |
    |   would    | character  |   would    |    life    |    well    |    best    | character  |   really   |    time    |   would    |
    | characters |    well    |  director  |    well    | character  |    well    |   films    | characters |    well    |    best    |
    |    life    |    life    | characters |   great    |   little   | characters |   scene    |    life    |   little   |   scene    |
    | character  |   scenes   |   really   |   films    |   films    |   films    |    life    |   scene    |   really   |    well    |
    |   people   |   little   |    life    | characters |    life    |   little   |   people   | character  |   scene    |   action   |
    |   scene    |    best    |   little   |   really   |   scenes   |   movies   |   little   |   little   |    year    | characters |
    |   movies   |    know    |   people   |    love    |   action   |  director  |   movies   |   people   | something  |   little   |
    |    best    |   really   |   films    |   world    |   people   |   great    |  another   |   films    |   people   |    know    |
    |   scenes   |   would    |   scenes   |   movies   |    work    |    year    |    well    |  director  |   seems    |   makes    |
    |   little   |   films    |   movies   |    know    |   seems    |    know    |   action   |    best    |   years    |  director  |
    |   action   |    made    |    made    |   little   |    love    |   script   |   really   |   still    |    know    |    love    |
    |  audience  |  another   |   think    |   people   |   really   |   scene    |   great    |  another   |    love    |    show    |
    |   great    |   scene    |    real    |    made    |  director  |    made    |   scenes   |   every    |   films    |   films    |
    |    love    |   action   |  another   |   seems    |   great    |   really   |    back    |   scenes   |    made    |    life    |
    |    know    |   movies   |   world    |   though   |    back    |    life    |    take    |  audience  |    back    |   still    |
    |   seems    |   great    | something  |    best    |   though   |   every    |    know    |    gets    |   movies   |   though   |
    +------------+------------+------------+------------+------------+------------+------------+------------+------------+------------+
    
Depois

    +------------+--------------+-------------+--------------+------------+------------+------------+------------+-------------+----------+
    |   Topic0   |    Topic1    |    Topic2   |    Topic3    |   Topic4   |   Topic5   |   Topic6   |   Topic7   |    Topic8   |  Topic9  |
    +------------+--------------+-------------+--------------+------------+------------+------------+------------+-------------+----------+
    |   marie    |   greatest   |    glory    |   lebowski   |   murphy   |    gere    |    epic    |    film    |    lucas    |  truman  |
    |   angela   |   portrait   |    walter   |  broderick   |  stillman  |  attorney  |    jake    |    time    |     jedi    | burbank  |
    | australian |     lucy     |   scorsese  |   bowling    |  invasion  |   derek    | ambitious  |    well    |    anakin   |  niccol  |
    |    mate    |    aaron     |    frank    |   buscemi    | marvelous  |   slave    |  portman   |   films    | astonishing |  shaft   |
    |   church   |    lounge    |    karen    |     coen     | australia  |  wahlberg  |  natalie   | character  |   knights   | colored  |
    |   exotic   |    neeson    |    miller   |    dating    |   reese    | friendship |   pacino   |   would    |   daniels   | charles  |
    |  ireland   |  bowfinger   |    scored   |    redman    |    gory    |    lucy    |   voiced   |    life    |     matt    | motives  |
    |   castle   |     mary     |   airplane  |    racism    |   multi    | adaptation |   naive    |   people   |   amidala   | cromwell |
    |   emily    |    cheek     |     shaw    | sentimental  |   donny    |    phil    | suspicion  | characters |   uniforms  | creator  |
    |    host    |    pride     |    palma    |    bunny     | carefully  |    nazi    |  sevigny   |   movies   |    cusack   | fabulous |
    |  releases  |     liam     |   serving   |    weight    |   shine    | anastasia  | kidnappers |   really   |    naboo    |  philip  |
    |    copy    |     lake     |     lama    |  confident   | commanding |   ramsey   | charlotte  |    best    |  perfection | gattaca  |
    |   pupil    |   federal    |   scarface  |    creeps    |    firm    |  coppola   | idealistic |   little   |   picking   | idyllic  |
    |   peace    |  groundhog   |   spending  | witherspoon  |   finely   |   report   |   desert   |    john    |   handsome  | mitchell |
    |  reynolds  |    jimmy     | charismatic | accompanying | apprentice |   cards    |  patterns  |  however   |   galactic  | despair  |
    |   nights   |   landing    |    hills    |    bound     |  cultural  |   memory   |  striking  |   world    |    libby    |   gere   |
    | henstridge | surroundings |   reminder  |   montana    |   dramas   |   chaos    | conditions |    made    |   florida   |   ford   |
    |   claude   |   colorful   |  strongest  |  redemption  |    loss    |  valjean   |  repeated  |   scene    |    empire   |   nail   |
    |   breed    |    month     |  defending  |   destined   | producing  |    hong    |   purely   |   great    |    darth    | educated |
    |   slick    |    robots    |    sixth    |    bowler    |    kiki    |    kong    |    andy    |   makes    |   freedom   |  prime   |
    +------------+--------------+-------------+--------------+------------+------------+------------+------------+-------------+----------+
    
Mac morpho:

    +------------+------------+------------+------------+------------+----------+------------+------------+------------+------------+
    |   Topic0   |   Topic1   |   Topic2   |   Topic3   |   Topic4   |  Topic5  |   Topic6   |   Topic7   |   Topic8   |   Topic9   |
    +------------+------------+------------+------------+------------+----------+------------+------------+------------+------------+
    |   paulo    |  editoria  |  segundo   |  editoria  |   página   |  página  |   página   |   página   |  editoria  |   sobre    |
    |   página   |   sobre    |   paulo    |   paulo    |  segundo   |  sobre   |  editoria  |   sobre    |   página   |   paulo    |
    |   sobre    |  segundo   |   página   |  segundo   |   sobre    |  brasil  |   sobre    |  editoria  |  segundo   |  editoria  |
    |  editoria  |   página   |   sobre    |   página   |  editoria  | editoria |   brasil   |   paulo    |   sobre    |   página   |
    |  segundo   |    anos    |   brasil   |    anos    |    anos    | segundo  |   paulo    |    anos    |   brasil   |   brasil   |
    |    anos    |   paulo    |  editoria  |   brasil   |   brasil   |  paulo   |  segundo   |  segundo   |    anos    |  segundo   |
    |  governo   |   brasil   |    anos    |  governo   |  milhões   |   pode   |    anos    |   brasil   |   paulo    |    pode    |
    |   brasil   |    pode    |   contra   |   sobre    |  governo   |   anos   |    dois    |    pode    |    pode    |    anos    |
    |    pode    |    dois    | presidente |    dois    |    pode    |   dois   |  governo   |  governo   |   contra   |    deve    |
    | presidente |    três    |    pode    | presidente |   paulo    | governo  | presidente |    dois    |   grande   |    dois    |
    |   contra   |   contra   |  governo   |  milhões   |    dois    |  parte   |    pode    |    três    |    dois    |   contra   |
    |  milhões   |  governo   |    deve    |   contra   | presidente |   três   |  milhões   |    país    |    três    |  governo   |
    |   maior    |    nova    |    dois    |    pode    |    real    |  outros  |   mundo    | presidente |    deve    |    três    |
    |    novo    |  milhões   |   mundo    |   fazer    |    país    |   país   |   contra   |  milhões   |    país    |    nova    |
    |    real    | presidente |   estado   |    três    |   outros   | pessoas  |   outros   |   tempo    |  governo   |   todos    |
    |    três    |   tempo    |    três    |    nova    |   maior    |  contra  |   folha    |   mundo    |  pessoas   |   outros   |
    |    dois    |   maior    |   maior    |  mercado   |   grande   |   deve   |    país    |    deve    | presidente |   mundo    |
    |    deve    |  mercado   |  dinheiro  |    deve    |   desde    |  fazer   |  mercado   |   contra   |   mundo    | presidente |
    |   todos    |    país    |   fazer    |   folha    |   mundo    | mercado  |   grande   | brasileira |   fazer    |    país    |
    |   fazer    |   fazer    |    país    |   grande   |   estado   |   nova   |   parte    |   maior    | ilustrada  |   fazer    |
    +------------+------------+------------+------------+------------+----------+------------+------------+------------+------------+
    
    
Depois

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
