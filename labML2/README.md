# Simulação Computacional dos Materiais - IFUSP
## Aula Lab ML2 - Descoberta de novos materiais com AM 

O objetivo desta aula será utilizar técnicas de aprendizado de máquina (AM) para a descoberta de novos materiais (*Materials Discovery*). A ideia é simples. Obtendo um bom modelo de regressão para uma propriedade alvo desejada (y) com base na composição do material (x1, x2 ... xn), é possível estimar o valor dessa propriedade para virtualmente qualquer material. Essa técnica permite, inclusive, avaliar combinações que nunca foram propostas anteriormente.

Projetos de aprendizado de máquina como este são usualmente divididos em quatro etapas: (1) obtenção dos dados, (2) criação de *features* (ou variáveis descritivas) que representem o problema (*feature engineering*), (3) obtenção de modelos e (4) aplicação dos modelos e avaliação final. Vamos dividir a atividade da mesma maneira:

### Etapa 1 - Banco de dados

Trabalharemos com um repositório de materiais de baterias chamado [Battery Explorer](https://materialsproject.org/#search/batteries), do Materials Project. O [banco de dados](./jobs/data) disponibilizado para a atividade contempla eletrodos compostos de até quatro elementos, excluíndo apenas Cl e Br (elementos tóxicos). A busca foi realizada considerando os seguintes intervalos: 


| Propriedade             | Property (EN)   | Intervalo      |
| ----------------------- |:---------------:| --------------:|
| Tensão média            | Average Voltage | -2, 9   (V)    |
| Capacidade volumétrica  | Capacity Vol    | 32-3200 (Ah/L) |
| Capacidade gravimétrica | Capacity Grav   |  6-680  (mAh/g)|

Para simplificar a atividade, a busca foi restrita a eletrodos com ions intercaláveis para uso em bateriais íons de lítio {sintaxe: *[intercalation: True, conversion: False, working ion: Li]*}. Mais de 2.000 entradas foram obtidas. A tensão (*Average Voltage*) associada a cada instância representa uma média das tensões de equilíbrio nos possíveis estados de carga (i.e. diferentes níveis de intercalação do íon de Li, e.g. Mn2O4, Li0-5(Mn2O4), LiMn2O4).

No diretório [/jobs/data](./jobs/data), você poderá verificar que o banco de dados foi obtido por meio de sete buscas distintas (*querys*), que foram integradas com o script **concat.py**. Se você tiver curiosidade, esse script tem alguns comandos interessantes utilizando a biblioteca *pandas*. O resultado desse processo foi exportado para os formatos **csv** e **json** (Dica: abra o arquivo Batteries_raw.csv para visualizar o banco de dados no estado atual).

**Dependências**

Como vamos utilizar os pacotes Keras e Tensorflow, o ideal é carregar o ambiente **deepmd** do conda, que já possuí tais bibliotecas, para economizar espaço.

```bash

conda env --list
conda activate deepmd

```

Para rodar o script **concat.py**, é necessário instalar (**pip3 install**) as seguintes bibliotecas externas:
- numpy
- pandas
- regex
- matminer


### Etapa 2 - Variáveis descritivas

Vamos analisar o banco de dados obtido na primeira etapa. Fica evidente que esse banco contém potenciais variáveis-alvo, que podem ser utilizadas para avaliar o desempenho de uma bateria, mas as únicas informações descritivas são a composição do material (Reduced Formula) e o grupo espacial (Spacegroup), que a estrutura cristalina do composto. Logo, precisamos utilizar métodos para construir variáveis descritivas com base nessas duas variáveis.

Nesta etapa, iremos utilizar a biblioteca **matminer** para criar *features* com base apenas na composição. Para tal, utilizaremos o script **feat_data.py**. Obs: no futuro, podemos adicionar informações estruturais para aumentar a complexidade do modelo, se achar necessário.

Os métodos a seguir serão implementadas para criar as variáveis descritivas: *ElementProperty, OxidationStates, AtomicOrbitals, BandCenter, ElectronegativityDiff, ElectronAffinity, ValenceOrbital, IonProperty, TMetalFraction*. Para saber mais, visite a [documentação do matminer](https://hackingmaterials.lbl.gov/matminer/).


```bash

python3 feat_data.py

```

Agora temos um banco de dados (Batteries_feat.json) com mais de 100 variáveis descritivas que podem ser utilizadas na etapa de modelagem.


### Etapa 3 - Modelagem


Chegou a hora de treinar o nosso modelo de regressão! Na verdade, não. Ainda precisamos instalar os módulos:
- matplotlib
- seaborn
- keras
- tensorflow

Agora abra o arquivo **load.py**, precisamos verificar algumas coisas antes de executá-lo. Na linha 26, podemos escolher qual banco de dados será carregado. Você pode usar o banco que acabou de obter com o script **feat_data.py**, e também pode usar o banco de dados **Batteries_final.json**, que contém duas variáveis descritivas adicionais, obtidas por meio dos métodos *CohesiveEnergy* e *AtomicPackingEfficiency*. Esses métodos são um pouco pesados computacionalmente, e requerem uma chave de acesso a API do Materials Project, por isso foram retirados (comentados) do script **feat_data.py**.

Observe também que, antes de iniciar o treinamento, as demais variáveis descritivas estão sendo excluídas do modelo. Isso ocorre pois elas podem ter um alto fator de correlação, e, além disso, tratando-se da descoberta de novos materiais, essas variáveis provavalmente serão desconhecidas.

Agora sim, chegou a hora de treinar nosso modelo executando o código:

```bash

python3 load.py

```

O código **load.py** está realizando uma implementação direta do método de árvores aleatórias (Random Forest), que pode ser modificado no arquivo **supplement.py**. O método *RandomForest* foi escolhido por se tratar de uma técnica simples, robusta, e o que pode ser treinada rapidamente. Fique a vontade para testar os conceitos da primeira aula em seu projeto e/ou para testar outras técnicas de AM. 


### Etapa 4 - Avaliação

Se tudo correu como deveria, você observou a criação de três gráficos no diretório do projeto. O primeiro gráfico mostra a importância relativa de cada *feature* para a floresta final. Os demais gráficos ajudam a visualizar a capacidade preditiva do modelo, na base de treino e de testes. Na sua opinião, o seu modelo conseguiu obter boas predições para a variável-alvo?


### Sugestões, comentários e relatório de atividades

Essa aula foi desenhada como uma breve introdução à modelagem de propriedades utilizando AM. Mas podemos ir além. Podemos modelar qualquer outra variável-alvo disponível no banco de dados inicial utilizando os recursos disponibilizados aqui. Escolha uma das seguintes variáveis para o seu relatório:

| Propriedade-alvo    | Grupo |
| ------------------- |:-----:|
| Capacity Grav       |   1   |
| Capacity Vol        |   2   |
| Specific E Wh/kg    |   3   |
| E Density Wh/l      |   4   |
| Stability Charge    |   5   |
| Stability Discharge |   6   |

Dica: para garantir um projeto único, mude o valor da variável **RSEED** nos scripts **supplement.py** e **load.py**. Essa variável pode ser igual a qualquer número inteiro: e.g. 424242. Não se esqueça de incluir a variável **Average Voltage** na matriz **excluded** (linha 36), uma vez que ela não será mais utilizada.

Por fim, você tem alguma ideia de como utilizar os modelos obtidos para a descoberta de novos materiais? Em caso de dúvidas, discuta com seus colegas :) 


## Agradecimentos

Esse projeto seria impossível sem os dados obtidos do [materials project](http://materialsproject.org/). Para mais informações sobre os dados, visite a [documentação do projeto Battery explorer](https://docs.materialsproject.org/user-guide/batteries-explorer/);

A obtenção do banco de dados dessa atividade foi realizada de maneira simplificada, como uma demonstração didática. Outra opção seria utilizar a biblioteca **pymatgen** para uma busca automatizada a partir da API (interface) do Materials Project. A vantagem de usar a API é que ela já retorna objetos **matminer**, poupando bastante tempo na hora as entradas de texto. Você pode obter sua chave pessoal para explorar o Materials Project [aqui](https://materialsproject.org/dashboard); 

Algumas referências que inspiraram esse tutorial:
- [arXiv:1903.06813v2](https://arxiv.org/pdf/1903.06813.pdf) [cond-mat.mtrl-sci].
- AIP Conference Proceedings 1765, 020009 (2016); [Hautier 2016](https://doi.org/10.1063/1.4961901).
- ChemDataExtractor. Sci Data 7, 260 (2020). [Huang & Cole 2020](https://doi.org/10.1038/s41597-020-00602-2).