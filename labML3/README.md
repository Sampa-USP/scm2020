# Simulação Computacional dos Materiais - IFUSP
## Aula Lab ML3 - Redes Neurais

Essa aula consiste em uma continuação da projeto iniciado na [aula 2](../labML2). Portanto, vamos utilizar o banco de dados Batteries_feat.json obtido na última aula. O objetivo é obter um modelo de regressão utilizando uma rede neural de três camadas, totalmente conectada. Para tanto, a primeira coisa que precisamos fazer é estudar o arquivo **supplement.py** (que foi atualizado!) para entendermos melhor como a rede neural é construída, otimizada e treinada utilizando o pacote [TensorFlow](https://www.tensorflow.org/).

```bash

cd scm2020/labML3
vim supplement.py

```

### Etapa 1 - Encontrando uma rede neural viável


O arquivo **supplement.py** possuí dois métodos para obtenção da rede neural. Vamos começar inspecionando o método **searchNN(X, y)** (linha 61). Essa função utiliza a rotina **RandomizedSearchCV** para buscar a melhor combinação de hiperparâmetros para a nossa rede. Trata-se de uma implementação simplificada, e o único parâmetro que está sendo otimizado é o número de neurons em cada uma das três camadas. Note que não há alteração na função de ativação (LeakyReLU), do otimizador (adam) ou da taxa de aprendizado.

Obs: em função da limitação de tempo para a aula, os modelos explorados durante a rotina RandomSearch estão sendo treinados por apenas 32 passos cada (epochs, linha 107). O interessante seria utilizar ao menos 100-200 passos para uma avaliação mais confiável de cada um desses modelos.

O método **searchNN** irá salvar o número de neurons do melhor modelo obtido durante a busca em um novo arquivo (**nn_raw.h5**) e irá retornar esse modelo.


### Etapa 2 - Treinando a rede neural

Agora basta passar o modelo com os parâmetros otimizados para o método **trainNN(model, X, y, steps)** e acompanhar o treinamento. Isso será feito por meio do script **load_NN.py**, que é muito similar ao script utilizado na aula passada. Pela construção do método **trainNN**, fica claro que devemos especificar o número de passos (*epochs*) desejados para o processo de treinamento. Para tal, basta alterar o último parâmetro na linha 74 do script **load_NN.py**.

Durante o treinamento, você irá verificar que o erro vai caindo, etapa a etapa. Não se preocupe em salvar esses dados, um registro do treinamento está sendo armazenado no arquivo *training.log*. 

Finalmente, o modelo final será salvo no arquivo **nn_trained.h5**.


### Etapa 3 - Avaliação da rede neural

Os mecanismos de avaliação implementados são os mesmos da última aula. Verifique os gráficos de correlação e erro, e compare-os com o modelo RandomForest.


### Etapa 4 - Fazendo previsões com os modelos obtidos

Para fazer previsões utilizando o modelo *RandomForest* treinado durante a última aula, utilize o script **predict_RF.py**. Na linha 19, adicione as composições que você gostaria de submeter ao modelo. No script original, você irá notar que quatro entradas do *Materials Project* já foram adicionadas para ajudá-lo a entender como os dados devem ser inseridos. A primeira coluna é uma *string* (texto) arbitrária usada para identificação. A segunda coluna, outra *string* que será posteriormente transformada na *Reduced Formula* e, portanto, deve seguir a formatação indicada (ElementoQuantidade Elemento2Quantidade ...).

O comando da linha 145 está utilizando pickle para carregar o modelo RF. Caso você queira testar o modelo de redes neurais que acabamos de treinar, substitua o comando pelas seguintes linhas para carregá-lo. O restante da implementação não deve mudar:

```bash

from keras.models import load_model
model = load_model('nn_trained.h5')

```

Dica: no VIM, digite 145gg para ir até a linha 145.


### Etapa 5 - Algumas questões

O que você acha que aconteceria se pudessemos treinar uma rede neural com capacidade (número de neurons) muito superior a essa que construímos hoje? Nesse caso, você acha que o desempenho poderia melhorar? 

Obs: na pasta 2048e, você irá encontrar uma rede neural com o número de neurons por camada limitado à 1000, e treinada por 2048 epochs. Se você tiver curiosidade, carregue o arquivo e compare com os seus resultados. Como ficou o erro na base de treino? E na base de testes? Compare os logs de treinamento para entender o que aconteceu.


## Agradecimentos

Esse projeto seria impossível sem os dados obtidos do [materials project](http://materialsproject.org/). Para mais informações sobre os dados, visite a [documentação do projeto Battery explorer](https://docs.materialsproject.org/user-guide/batteries-explorer/);

A obtenção do banco de dados dessa atividade foi realizada de maneira simplificada, como uma demonstração didática. Outra opção seria utilizar a biblioteca **pymatgen** para uma busca automatizada a partir da API (interface) do Materials Project. A vantagem de usar a API é que ela já retorna objetos **matminer**, poupando bastante tempo na hora as entradas de texto. Você pode obter sua chave pessoal para explorar o Materials Project [aqui](https://materialsproject.org/dashboard); 

Algumas referências que inspiraram esse tutorial:
- [arXiv:1903.06813v2](https://arxiv.org/pdf/1903.06813.pdf) [cond-mat.mtrl-sci].
- AIP Conference Proceedings 1765, 020009 (2016); [Hautier 2016](https://doi.org/10.1063/1.4961901).
- ChemDataExtractor. Sci Data 7, 260 (2020). [Huang & Cole 2020](https://doi.org/10.1038/s41597-020-00602-2).
