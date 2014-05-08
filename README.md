Fundação Getúlio Vargas

Modelagem de Assuntos

Profº Flavio 

Aluno: Sérgio da Silva Rodrigues

===

Objetivo
Modelagem de Assuntos utilizando o Latent Dirichilet Algorithm

Dataset 
Obras literárias de Machado de Assis, obtidas da biblioteca NLTK.

Ferramentas utilizadas
Python 2.7
Bilbioteca NLTK
Biblioteca GENSIM

Descrição
O corpus das obras do escritor Machado de Assis contém uma coleção de 137 contos, 45 críticas literárias, 24 crônicas, 7 poesias, 10 peças de teatro, 10 miscelâneas, 3 traduções e 10 romances, totalizando 246 documentos. 
Os documentos foram pré processados para remover palavras indesejadas como preposições, interjeições e outras de pouco valor semântico ao interesse da análise. Estas palavras estão registradas no arquivo stopwords_pt.txt.
Após a removação das palavras comuns, cada documento foi tokenizado e armazendo em disco para futuras referências.

Devido a quantidade de documentos a processar, decidimos realizar um pré processamento 
dos documentos, removendo  foi utilizado o LDA da biblioteca GENSIM.
