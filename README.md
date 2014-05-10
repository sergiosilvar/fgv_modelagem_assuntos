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

<code>
    texts = documentos(pasta)
    
    dictionary = corpora.Dictionary(texts)
</code>

. Essa estrutura atribui um número ineitor como identificador exclusivo a cada palavra utilizada nos documentos, em nosso caso, a cada palavra nos documentos após o pré processamento. Em seguida, 




, que *bag-of-words*,  repositório de palavras,

Devido a quantidade de documentos a processar, decidimos realizar um pré processamento 
dos documentos, removendo  foi utilizado o LDA da biblioteca GENSIM.
