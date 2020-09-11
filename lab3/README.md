# Simulação de metano em alta pressão com dinâmica molecular

## Objetivos

- Introduzir o aluno à simulações com dinâmica molecular
- Entender a estrutura básica dos arquivos necessários para uma simulação com o LAMMPS
- Realizar a minimização de energia de uma molécula
- Realizar uma simulação do gás metano em alta pressão, obtendo a distribuição radial de pares, o coeficiente de auto-difusão com a fórmula de Einstein e a viscosidade com Green-Kubo

## Minimização de energia

Para fixar o conceito de campo de forças apresentado em aula e apresentar os arquivos de entrada do LAMMPS, vamos realizar uma minimização de energia de uma molécula.


## Simulação de metano considerando diferentes temperaturas e pressões

### Densidade e temperatura da simulação

Aluno | Temperatura (K) | Densidade (kg/m^3)
----- | --------------- | ------------------
1     | 273.15          | 50
2     | 273.15          | 100
3     | 273.15          | 150
4     | 273.15          | 200
5     | 273.15          | 250
6     | 273.15          | 300
7     | 273.15          | 350
8     | 273.15          | 400
9     | 273.15          | 450
10    | 273.15          | 500
11    | 273.15          | 550
12    | 273.15          | 600
13    | 303.15          | 50
14    | 303.15          | 100
15    | 303.15          | 150
16    | 303.15          | 200
17    | 303.15          | 250
18    | 303.15          | 300
19    | 303.15          | 350
20    | 303.15          | 400
21    | 303.15          | 450
22    | 303.15          | 500
23    | 303.15          | 550
24    | 303.15          | 600


## Criando arquivos de entrada

### Determinando o tamanho da caixa

O tamanho da caixa deve ser determinado à partir da densidade a ser simulada.
Como a caixa é gerada replicando uma caixa com somente uma molécula, precisamos calcular o volume ocupado por uma molécula de metano condirando uma certa densidade.
Para isso calculamos o volume molar do metano, e dividimos pelo número de Avogadro, obtendo então o volume ocupado por uma molécula.
Com isso, podemos calcular qual o lado de uma caixa cúbica contendo uma única molécula de metano que dá aquela densidade.

Sumarizando, podemos obter o lado da caixa cúbica correspondente a uma certa densidade de metano com:

<img src="https://render.githubusercontent.com/render/math?math=%5Cleft(%5Cfrac%7B160424.6%7D%7B6.022%5Crho%7D%5Cright)%5E%7B1%2F3%7D">

sendo <img src="https://render.githubusercontent.com/render/math?math=%5Crho"> a densidade de metano (em kg/m<sup>3</sup>) desejada para a simulação.
