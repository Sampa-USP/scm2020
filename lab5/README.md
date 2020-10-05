# Mecânica Quântica, Soluções da equação de Schrödinger em 1-D e dispositivos eletrônicos

Nesse laboratório, utilizaremos uma aplicação em Java que resolve em tempo
real a equação de Schrödinger para uma partícula em uma dimensão. A
aplicação nos permite variar o potencial externo e visualizar as soluções das
funções de onda, posição e momento da partícula.

O aplicativo foi desenvolvido como material de apoio do livro "Visual Quantum
Mechanics" - Bernd Thaller.

O objetivo desse laboratório é desenvolver uma intuição em relação a Mecânica
Quântica através da visualização das soluções da Eq. de Schrödinger para
situações de interesse em Ciência dos Materiais:

1. Poço finito
2. Poço acoplado duplo
3. Poço acoplado duplo com campo elétrico
4. Série de poços finitos
5. Efeito de impurezas
6. Efeito de discordâncias

Como aplicações dessas situações, temos o problema de um elétron sobre um
potencial periódico. A solução desses problemas nos leva diretamente a idéia de
bandas eletrônicas, onde de acordo com o preenchimento dessas bandas os
materiais podem ser classificados como metais, semimetais, semicondutores e
isolantes.

Essas simulações também nos permite entender o funcionamento de alguns
dispositivos opto-eletrônicos como lasers semicondutores, diodos, células
solares e dispositivos baseados em heterojunções semicondutoras.

Para cada um dos potenciais acima, iremos gerar um pacote de ondas
gaussiana (equivalente a descrevermos por exemplo um elétron) e observarmos
a dispersão desse pacote e a localização e forma do estado fundamental e o
primeiro estado excitado. Descreva para cada potencial e os parâmetros a ele
associado, o comportamento dos níveis de energia e da dispersão do pacote de
ondas.


Para seguir os próximos passos entre no index.html com o Firefox:

```bash
firefox html/index.html &
```

## Caso 1: Poço finito (Finite Well)

Com o mouse, crie um pacote de ondas gaussianas (Create Gaussian). Observe
o que ocorre com uma partícula de massa leve (modifique o botão da massa
para esquerda) variando:

- Largura do poço (well width) (largo e estreito com a profundidade
intermediária)
- Profundidade do poço (depth width) (profundo e raso com a largura
intermediária)

## Caso 2: Poço acoplado duplo (Coupled Well Pair)

Como no caso anterior, crie com o mouse um pacote de ondas gaussianas
(Create Gaussian). Observe o que ocorre com uma partícula de massa leve
(modifique o botão da massa para esquerda) variando:

- Separação entre os poços (próximo e afastado)
- Potencial da parede (baixo e alto)

## Caso 3: Poço acoplado duplo com campo (Coupled Wells + Field)

Nesse caso, alterando-se o campo aplicado, criamos uma distorção nos poços.
Varie o valor do campo aplicado e o efeito da separação entre os poços.
Compare com o caso anterior (caso 2).

## Caso 4: Série de poços finites (Well Array (Square))

- Também comparando-se com o caso 2, qual o efeito de termos uma
série de poços periódicos ?

## Caso 5: Impurezas (Well Array w/ Impurity).

Nesse caso, queremos analisar o efeito de uma impureza. Observe o que ocorre
com o pacote de ondas quando é localizado próximo e afastado da impureza.

##Caso 6: Discordância (Well Array w/ Dislocation)

Repita o mesmo que o caso 5 com um potencial que descreve o efeito de uma
discordância.