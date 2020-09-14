# Simulação de metano em alta pressão com dinâmica molecular

Neste laboratório vamos estudar o comportamento do metano em condições de alta pressão.
Para isso, vamos utilizar simulações de dinâmica molecular e comparar os resultados obtidos com resultados disponíveis na literatura.
Este laboratório dá sequência ao [laboratório 2](../lab2), tenha certeza de ter entendido o conteúdo antes desse laboratório antes de prosseguir.

Estaremos interessados em observar propriedades dependentes de médias temporais.
Especificamente, vamos calcular o coeficiente de auto-difusão e a viscosidade nas diferentes condições de simulação.
Para isso, faremos simulações no ensemble *NVT*, simulando em diferentes densidades.
Como o volume é mantido constante nesse tipo de simulação, diferentes densidades são equivalentes a diferentes pressões.
Nesse caso, a pressão será uma das propriedades que podemos obter com a simulação.

## Objetivos

- Introduzir o aluno à simulações com dinâmica molecular.
- Realizar uma simulação do gás metano em alta pressão, obtendo a distribuição radial de pares, o coeficiente de auto-difusão com a fórmula de Einstein e a viscosidade com Green-Kubo.

## Simulação de metano considerando diferentes temperaturas e pressões

Para obter curvas de como as propriedades que estudaremos variam com a temperatura e pressão, cada aluno vai realizar a simulação em uma temperatura e pressão conforme a tabela abaixo.

Aluno | Temperatura (K) | Densidade (kg/m<sup>3</sup>)
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


## Arquivos de entrada para a simulação

Como cada aluno deverá simular em uma diferente condição termodinâmica, os arquivos de entrada deverão ser preparados adequadamente para cada caso.

### Topologia

Conforme visto no laboratório anterior, o arquivo de topologia contém as informações sobre a composição do sistema e como os átomos do sistema interagem.
Como estaremos estudando o mesmo sistema, a parte de topologia que descreve as interações será a mesma.
Entretanto, fixado um número de moléculas, como as simulações ocorrerão em diferentes densidades, teremos diferenças com relação ao tamanho da caixa de simulação para obter a densidade desejada.
Na próxima seção explicaremos como determinar o lado da caixa.

Abra o arquivo `metano.lmp`, visualize a topologia e compare a topologia da molécula de metano do [laboratório 2](../lab2).
Você deve notar que a topologia `metano.lmp` utilizada neste exercício possui **um único átomo**!
Isso é devido a uma aproximação adicional, que estamos fazendo para reduzir o custo computacional.
Utilizaremos nesse laboratório um modelo **united atom (UA)** para o metano.

Este tipo de modelo, utiliza-se do fato de que os hidrogênios de hidrocarbonetos interagem pouco com outros átomos e moléculas (por exemplo, não formam ligação de hidrogênio) para incluí-los de maneira efetiva no potencial do carbono.
No caso do metano, isso significa que temos um único "átomo" do tipo `CH4`.
Esse átomo `CH4` possui a massa da molécula de metano e um <img src="https://render.githubusercontent.com/render/math?math=%5Cepsilon"> e <img src="https://render.githubusercontent.com/render/math?math=%5Csigma"> diferentes para tentar compensar pela falta de átomos de hidrogênio.

Utilizar modelos UA significa reduzir consideravelmente o custo computacional da simulação.
Isso porque temos menos átomos interagindo (neste caso apenas 1/5 dos átomos), e também permite utilizar um *timestep* para integração ligeiramente maior, por não precisar considerar o tempo característico das vibrações dos átomos de hidrogênio.


### Determinando o tamanho da caixa

O tamanho da caixa deve ser determinado à partir da densidade a ser simulada.
Como a caixa é gerada replicando uma caixa com somente uma molécula, precisamos calcular o volume ocupado por uma molécula de metano condirando uma certa densidade.
Para isso calculamos o volume molar do metano, e dividimos pelo número de Avogadro, obtendo então o volume ocupado por uma molécula.
Com isso, podemos calcular qual o lado de uma caixa cúbica contendo uma única molécula de metano que dá aquela densidade.

Sumarizando, podemos obter o lado da caixa cúbica correspondente a uma certa densidade de metano com:

<img src="https://render.githubusercontent.com/render/math?math=%5Cleft(%5Cfrac%7B160424.6%7D%7B6.022%5Crho%7D%5Cright)%5E%7B1%2F3%7D">

sendo <img src="https://render.githubusercontent.com/render/math?math=%5Crho"> a densidade de metano (em kg/m<sup>3</sup>) desejada para a simulação.
