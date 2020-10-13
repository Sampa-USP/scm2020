# Laboratório 6: Cálculos de Primeiros Princípios. 

## O que eu posso aprender neste tutorial?

1. Como executar PWscf (pw.x) no modo autoconsistente para o Silício;
2. Como lidar com metais (Alumínio);
3. Como calcular a energia de interação entre homodímeros de metanol usando computação voluntária e desenvolver um campo de força;

 **Objetivo: formar usuários independentes do pacote Quantum-ESPRESSO <http://www.pwscf.org>**
 
 Utilizaremos os arquivos executáveis já disponíveis na máquina virtual:
1) **pw.x** = arquivo executável para cálculos de primeiros princípios;
2) **bands.x** = arquivo executável para determinar as bandas eletrônicas do sistema;
3) **ev.x** = calcula a equação de estado; 
4) **pp.x** = realiza o pós-processamento para visualizar a estrutura de bandas;
5) **plotrho.x** = visualiza a densidade de carga do sistema;
6) **plotband.x** = faz o gráfico da estrutura de bandas do sistema;

**Obs: Todas as linhas, após $, devem ser escritas pelo usuário na linha de comando.**

Para rodar pw.x:

```bash
pw.x < input > output
```

Para rodar bands.x:

```bash
bands.x < input > output
```

* Densidades e temperatura são dadas em unidades atômicas: Energia (Rydberg) e Comprimento (Bohr).

### ARQUIVOS DE SAÍDA:
O arquivo de saída de `pw.x` nos fornece todas as informações sobre a estrutura eletrônica do sistema bem como resume as informações de entrada, geometria, forças e tensões sob os átomos.
 **É muito importante deixar a pasta Lab6 no /home/sampa para evitar alguns bugs!**

## Sistema 0: Testes iniciais com uma molécula de metanol

Nesta prática de laboratório iremos otimizar uma molécula de metanol

**1.** Entre no diretório `lab6/Metanol/molecula_isolada` e abra com o seu editor de preferência ou entrada `espresso.in`;

**2.** Use o Xcrysden para visualizar uma estrutura no arquivo de amostra:

```bash
$ xcrysden --pwi espresso.in &
```

observe uma estrutura, como posições atômicas da molécula. Crie uma estrutura, explore o menu do software.

**3.** Para executar o código:

```bash
$ pw.x <espresso.in> espresso.out
```

## Sistema 1: Testes iniciais com o Silício Si
Nesta prática de laboratório iremos calcular algumas propriedades para o Silício. Você encontrará dentro da pasta `lab6/Si` arquivos com três diretórios (Estrutura, Bulk_Modulus e Bandas), os quais serão utilizados nas tarefas desta prática.

**Esses arquivos contém:**

* Estrutura:  diretórios com os inputs para o Exercício 1;
* Bulk_Modulus:  diretórios com os inputs para o Exercício 2;
* Bands: diretórios com os inputs para o Exercício 3;

### Tarefa 1: Estrutura: convergência  do cutoff e pontos  K

Nesta tarefa iremos calcular a energia total para o silício, através do cálculo autoconsistente (scf). Faremos dois testes de convergência:

1. Convergência dos raios de corte (cutoffs) para as funções de onda:  (“ecutwfc”)
2. Convergência da energia total e pontos K (k-points)

Entre no diretório  `lab6/Si/Estrutura` e abra com o seu editor de preferência o input `si.scf.in`:
1. Utilize o software XCRYSDEN para visualizar a estrutura:
digite no terminal `xcrysden`;
2. Abra o menu `File > Open PWscf > Open PWscf input file`
3. Selecione seu arquivo de input.
4. Observe a estrutura, as posições atômicas na célula unitária. Gire a estrutura, explore o menu do software;
5. Abra o arquivo de texto e observe algumas informações relevantes:

* **ibrav =2**: define o tipo de célula, 2 corresponde ao tipo cúbica de face centrada (fcc, face centered cubic): v1 = (a/2)(-1,0,1) v2 = (a/2)(0,1,1) v3 = (a/2)(-1,1,0);
*  **celldm(1)=10.2625**,  define o parâmetro a= 10.2625 bohr (1 bohr = 0.529177 Å);
* **nat=2**: número de átomos na célula;
*  **ntyp=1**: tipo de átomos do sistema
*  **Si 28.0855 Si.pbe-rrkj.UPF**:  pseudopotencial do Silício;
*  **ATOMIC_POSITIONS (alat)**:   as posições atômicas dos átomos da célula estão nas coordenadas cartesianas, em unidades do parâmetro de rede;
*  **conv_thr=1d-8**: Limite de convergência do cálculo scf. estimated energy error > conv_thr (NO) or energy error < conv_thr (YES);

### Parte A:  convergência  do cutoff 

A energia de corte para ondas planas (ecutwfc) determina o valor máximo da energia cinética das ondas planas incluídas no cálculo. Como este conjunto de bases é infinito, realizaremos testes de convergência da energia potencial (energia de KS) para determinar o valor de **ecutwfc** para o qual as funções de base de ondas planas serão truncadas.

**Exercício**: Edite o input si.scf.in, e estude diferentes valores de ecutwfc

**A1** - Execute o código para alguns valores de ecutwfc, para obter  o valor da energia. Salve o valor de energia para cada valor ecutwfc, no arquivo `si.etotvsecut`

Neste exemplo, você pode tentar alguns valores de ecutwfc (em Ry):
16
20
24
32

Para executar o código: 

```bash
$ pw.x <si.scf.in > si.scf.out
```

**A2**.  Preencha os dados no arquivo **si.etotvsecut**;

**A3**. Plote o arquivo si.etotvsecut usando seu programa de plotagem preferido.

**A4**. Discuta o resultado

### Parte B: convergência  do  K-points

Para considerar corretamente a periodicidade do sistema, é necessário um conjunto de pontos K suficientemente denso.

**B1** Edite o input `si.scf.in` (defina ecutwfc para 12 Ry), modificando o grid de K_POINTS para usar Monkhorst-Pack grids: 
* K_POINTS tpiba
* K_POINTS automatic
* nk1 nk2 nk3 k1 k2 k3
* com nk1=nk2=nk3=2, 4, 6, 8, 10, 12 (número crescente de k-points), k1=k2=k3=1;]

**B2**- Execute `pw.x`, **complete as entradas no arquivo si.etotvsnks**  (nks é o número real de k-points na BZ irredutível usados no cálculo, impressos no output)

**B3**- Plote a coluna 3 vs coluna 1, para obter o gráfico energia versus nks

### Tarefa 2: Cálculo de Bulk Modulus

Nesta parte iremos explorar propriedades mecânicas do sistema através da Equação de estado de F. D. Murnaghan ( Proc. Nat. Acad. Sci. USA, 30, 244 (1944))

Entre no diretório  Lab6/Si/Bulk_modulus;

**2.1** Edite o arquivo de entrada, `si.in`, com cutoff e nks obtidos na tarefa 1. Efetue cálculos scf para um conjunto de constantes de rede diferentes, para obter  o mínimo de energia. Salve o valor de energia para cada constante de rede, no arquivo bulk_modulus_Si.dat 

**Neste exemplo, você pode tentar alguns valores de constante de rede (em bohr)**:
Valores|
:-:
9.8|
10.1|
10.2|
10.3|
10.7|

**2.2** - Salve o valor de energia para cada valor de parâmetro de rede no arquivo `bulk_modulus_Si.dat` para gerar um gráfico de energia versus constante de rede.

Edite o arquivo `bulk_modulus_Si.dat` com seu editor de texto favorito e mantenha apenas as informações da constante de rede (em bohr) e energia (em Ry).

Agora para obter a equação de estado de Murnaghan 

Aqui fazemos duas propostas para analisar a equação de estado de Murnaghan:

**(i)** digite `ev.x`, e forneça as informações do sistema:

*  Lattice parameter or Volume are in (au, Ang) >  au 
*  Enter type of bravais lattice (fcc, bcc, sc, noncubic) > fcc
*  Enter type of equation of state : 1=birch1, 2=birch2, 3=keane, 4=**murnaghan** > 4
*  Input file >  bulk_modulus_Si.dat
*  Output file > new.dat

* Compare os resultados obtidos de bulk modulus, constante de rede com dados teóricos e experimentais  da literatura. Dica: J. Junquera et al., Phys. Rev. B 64, 235111 (2001) 

**(ii)** Uma maneira que pode ser utilizada tanto no quantum espresso quanto em outros programas:

Nesta parte iremos "brincar" com as unidades do arquivo `bulk_modulus_Si.dat`. Iremos converter a energia para eV (1Ry=13.605 eV) e o parâmetro de rede para angstroms (1 bohr = 0.529177Ang). Essa conversão pode ser realizada através do xmgrace:

Selecione: data >>> transformations>>>evaluate expression
Na caixa: evaluate expression
1. Selecione os dois set
2. Edita a seguinte Fórmula `x = x * 0.529177` e clica em apply
3. Edita a seguinte Fórmula `y = y * 13.605` e clica em apply
4. Salva 
5. No editor vim apague todas as linhas que começam com @/& use o comando 320dd. Deixando apenas as linhas com os valores de energia e parâmetro de rede. 
6. Introduza na primeira linha deste arquivo o tipo de Bravais lattice do sistema em estudo (sc, bcc, fcc ou diamond).
Para o presente exemplo, Si, seria  diamond.

* Execute o script para ajustar os dados de energia versus volume ao
Equação do estado de Murnaghan.

```bash
$ python fit_results.py bulk_modulus_Si.dat 
```

O resultado é um gráfico com os pontos calculados, a curva de ajuste e os valores:
volume no mínimo (em Angstrom ^ 3),
o módulo de bulk (em eV / Ang ^ 3; Lembre-se de que 1 eV / Ang ^ 3 = 160,2176487 GPa),
a energia no mínimo (em eV),
 a derivada de pressão do bulk modulus no volume de equilíbrio,
e a constante de rede.

* Uma figura pode ser gerada automaticamente escrevendo o nome do
arquivo de destino. Vários formatos são permitidos (pdf, gif, jpeg, ...)


* Compare os resultados obtidos de bulk modulus, constante de rede com dados teóricos e experimentais  da literatura. Dica: J. Junquera et al., Phys. Rev. B 64, 235111 (2001) 


### Tarefa 3: Estrutura de Bandas

Neste exercício, examinaremos algumas informações 'pós-processamento' que você pode fazer depois de executar seus cálculos scf. Aqui veremos algumas outras informações que podemos extrair dos arquivos produzidos quando se faz um cálculo PW,  por exemplo, densidades de carga e autovalores (que usaremos para obter gráficos de estrutura de banda e densidades de estados). 
Entre no diretório Bandas
* Si.scf.in: arquivo de entrada para cálculos scf.
* bands.in: arquivo de entrada para obter as bandas.
* k-point-path: arquivo que contém uma lista de k-points ao longo de direções de simetria na zona de Brillouin.
* Si.plotband.in: arquivo de entrada para colocar os dados da estrutura da banda em um formato plotável.
* Si.pp_rho.in: arquivo de entrada para extrair a densidade de carga usando o pós-processamento.
* Si.plotrho.in: arquivo de entrada para traçar a densidade de carga.
* dos.in: arquivo de entrada para calcular a densidade de estados.

**(a) Cálculos autoconsistentes (scf) para Si**
 **3.1** Abra e leia o arquivo de amostra `Si.scf.in`
 **3.2** Escolhemos os valores de celldm (1), ecutwfc, nk1, nk2 e nk3 com base em nossos resultados obtidos na tarefa 1. Você pode escolher os mesmos valores que estes ou substituir seus valores.
 **3.3** Execute o cálculo de scf
 $  pw.x <Si.scf.in> Si.scf.out

**(b) Estrutura de bandas do Si**
 **3.4** Abra o arquivo Si.band.in
 **3.5** Leia e confira as modificações realizadas neste arquivo Si.band.in 
 
* Para realizar os cálculos não autoconsistentes (nscf), os quiasserão usados ​​para obter a estrutura da banda, configurando o arquivo **calculation = 'bands'**.
* Utiliza-se o **nbnd = 8**, à lista de nomes & SYSTEM para especificar o número de bandas calculadas. Observe que para uma célula de Si de 2 átomos, temos 8 elétrons e, portanto, apenas 4 bandas ocupadas, mas vamos calcular algumas bandas extras (vazias).
* O  **K_POINTS** para especificar o caminho ao longo das direções de simetria na zona Brillouin. Para isso, você pode usar as informações fornecidas no arquivo chamado caminho do ponto-k, que contém uma lista de pontos-k ao longo de direções de alta simetria no BZ, ou seja, L (½, ½, ½) para Gama ( 0, 0, 0) a X (0, 0, 1) a W (0, ½, 1) a X (0, 1, 1) a Gama (0, 0, 0). Você pode colar esse arquivo em **Si.band.in** após o cartão ** K_POINTS**.
 
 **3.6** Execute o cálculo de 'bandas':

```bash
$ pw.x <Si.bands.in> Si.bands.out
```

* Que diferenças você vê entre o arquivo de saída obtido aqui e o arquivo de saída obtido com o cálculo de scf?
**3.7** Aqui, iremos coletar algumas informações para plotar a estrutura de bandas
* Olhe para o arquivo bands.in
* Observe que você deve usar o mesmo prefixo neste cálculo que foi usado nos cálculos de bandas AND de scf.
* A bandeira **filband** define o nome do arquivo no qual os dados das bandas são armazenados.
* Caso ocorra algum erro, é necessário informar em outdir o endereço completo dos arquivos terminados em .wfc1, por exemplo **outdir** = '/home/sampa/Lab6/Si/outdir'.

**Execute**

```bash
$ bands.x <bands.in> bands.out
```

Dê uma olhada em bands.out e bands.dat e observe os autovalores de  mínimo e máximo de energia em diferentes pontos k.
**3.8** Agora vamos obter os dados em um formato para plotar
Abra o input  **Si.plotband.in**, o arquivo contém:


* arquivo de entrada (= bands.dat obtido na etapa anterior).

* Emin e Emax (= -6,00 e 10,00).
arquivo de saída no formato xmgrace (bands.xmgr)
* arquivo de saída no formato ps (bands.ps)
* Energia de Fermi (= 6,337 eV)
* deltaE e energia de referência (= 1,00 6,337)

**Execute o programa de plotagem:**

```bash
$ plotband.x <Si.plotband.in> Si.plotband.out
```

Você pode ver a estrutura da banda desenhada no formato ps (bands.ps) usando um visualizador de postscript (por exemplo, ghostview, ggv, ou o editor de pdf).

**(c) Densidade de carga para S**i 

* **3.9** Agora fazemos o pós-processamento para extrair a densidade de carga

* Abra o arquivo `Si.pp_rho.in`
* Certifique-se de que o valor do prefixo seja igual aos valores usados ​​nos cálculos de scf.
* **filplot = 'Si.charge'** salva a densidade de carga extraída e é usado para plotagem definindo **filepp (1) = 'Si.charge'** e os dados a serem plotados escritos em **fileout = 'Si.rho.dat'** .
* **plotnum =0** indicates that the quantity to be extracted is the charge denisty (for other possible options, see INPUT_PP).
* **iflag** e **output_format** especificam a dimensionalidade do gráfico.
* e1 (i) e e2 (i) (i = x, y e z) são vetores 3D que determinam o plano de plotagem e devem ser ortogonais entre si.
* nx e ny são o número de pontos no plano.

**Execute o código de pós-processamento:**

```bash
$ pp.x <Si.pp_rho.in> Si.pp_rho.out
```

Veja o arquivo **Si.rho.dat**

**Execute o código de plotagem:**

```bash
$ plotrho.x <Si.plotrho.in> Si.plotrho.out
```

Use ghostview, ggv ou algum arquivo de pdf para ver a densidade de carga do Si Si.rho.ps
.
 
**(d) Gráfico da densidade de estados do Si**
* Primeiro execute um cálculo nscf para obter os estados do DOS
* Copie Si.scf.in para Si.nscf.in
* Altere o cálculo do sinalizador = **'nscf'**
* Altere o número de bandas para adicionar alguns estados vazios na lista de nomes & SYSTEM (nbnd = 8).
* Defina **occupations='tetrahedra’** na lista de nomes & SISTEMA.
* Modifique o  **K_POINTS** de '6 6 6 1 1 1' para '12 12 12 1 1 1 ', porque agora queremos calcular os valores próprios em uma malha mais fina no espaço k.
* Lembre-se de que as mesmas funções de onda (conforme obtidas nos cálculos de scf) devem ser usadas, portanto, **NÃO mude o prefixo.**

**Execute os cálculos nscf:**

```bash
$ pw.x <Si.nscf.in> Si.nscf.out
```

### Cálculos DOS

3.10 Abra o arquivo **dos.in**

* Certifique-se de que tem o mesmo prefixo usado nos cálculos de nscf.
* Os resultados do DOS são escritos em **fildos = (dos.dat)**
* Caso ocorra algum erro, é necessário informar em **outdir** o endereço completo dos arquivos terminados em, por exemplo outdir = '/home/sampa/Lab6/Si/outdir'
 
**Execute cálculos de densidade de estados:**

```bash
$ dos.x <dos.in> dos.out
```

* Dê uma olhada em `dos.out` e o arquivo de dados `dos.dat`.
* Plote o arquivo dos.dat para ver o gráfico do DOS (você pode usar os programas gnuplot ou xmgrace).

**Discuta os resultados obtidos nesta etapa**
 
## Sistema 2: Testes com o Alumínio 

Nesta prática de laboratório iremos calcular algumas propriedades para metais, em especial o Alumínio (Al). Você encontrará dentro da pasta `lab6/Al` arquivos com três diretórios (Estrutura, Bulk_Modulus e Bands), os quais serão utilizados nas tarefas desta prática.

### Tarefa 1: Estrutura: convergência  do cutoff e pontos  K

Nesta tarefa iremos calcular a energia total para o Alumínio, através do cálculo autoconsistente (scf). Faremos dois testes de convergência:

* 1.  Convergência dos raios de corte (cutoffs) para as funções de onda:  ("ecutwfc")
* 2.  Convergência da energia total e pontos K (k-points)

Entre na pasta Al/Estrutura, 
Você verá os seguintes arquivos:

**Al.sample.in**  este é um arquivo de entrada de amostra, para uma célula Al primitiva.

Algumas informações sobre o input:

Em comparação com os arquivos de entrada para o Si (tarefa 1, exercício 1), existem duas diferenças principais:

**(i)** Agora **nat = 1** em vez de **nat = 2** e, consequentemente, há apenas um átomo de Al em 0,0 0,0 0,0

**(ii)** Existem linhas adicionais, dizendo que a ocupação deve ser smearing width, que tipo de smearing usar e que valor de **desmagnetização** (largura da smearing ) usar.
Note que agora nós definimos **verbosity = 'high'** na lista de nomes do & control ; para que o código imprima os números de ocupação, etc.


**1.** Use o Xcrysden para visualizar a estrutura no arquivo de amostra:

```bash
$ xcrysden --pwi Al.sample.in &    
```

Responda: Quantos átomos estão contidos na célula cúbica convencional?

**2**.   Execute um cálculo scf:
```bash
$ pw.x <Al.sample.in> Al.sample.out
```

**3**.  Leia a saída e responda às seguintes perguntas:
*  **3.1**. Quantas bandas foram calculadas? Como isso se compara ao número de elétrons?
* **3.2**. Qual é a energia Fermi? 

**4.** Faça os testes de convergência em relação ao corte de onda plana:

Em princípio, você deve agora executar uma série de cálculos com diferentes valores de ecutwfc (como fez para Si) e ver em qual valor de ecutwfc sua energia total convergiu. No entanto, para economizar tempo, vamos supor que isso tenha sido feito. Continue trabalhando com ecutwfc = 12 .

**5.**  Agora faça os testes de convergência em relação à amostragem da zona de Brillouin  e smearing width:
Vamos decidir simultaneamente qual malha de k-pontos (valores de nk1, nk2, nk3 ) e o valor de smearing width (degauss) usar. Para simplificar, vamos supor agora que usaremos apenas o  smearing  Marzari-Vanderbilt.

* 5.1**. Vamos calcular um loop de nk1, nk2, nk3 = 6 6 6, 8 8 8, 12 12 12, 16 16 16
* Para cada uma dessas malhas de k-pontos, faça um loop sobre degauss variando de 0.02 a 0.10 (em intervalos escolhidos por você).
* Para cada valor de malhas de k-pontos teremos um arquivo al.m-p.nks (por exemplo, al.m-p.12 nk1, nk2, nk3 = 12 12 12 ) que contém duas colunas, a primeira  contém o  degauss, e a segunda contendo a energia total.
** Observação: Nós já calculamos algumas malhas de k-pontos usando um loop sobre os  degauss variando de 0,02 a 0,10. Abra os arquivos:
  * al.m-v.6 que corresponde nk1, nk2, nk3 = 6 6 6 e calcule a energia para os valores de degauss que faltam no arquivo;
 * al.m-v.8 que corresponde nk1, nk2, nk3 = 8 8 8 e calcule a energia para os valores de degauss que faltam no arquivo;
 * nk1, nk2, nk3 = 12 12 12, 16 16 16 os cálculos estão completos**

**5.2.** Faça um gráfico mostrando como a energia total varia com o número de pontos k e com o degauss , usando um programa de plotagem de sua escolha. 

**O mesmo pode ser realizado usando o  smearing  gauss (arquivos, al.g.) e methfessel-paxton (arquivos, al.m-p.)**
O resultado convergente 'verdadeiro' é obtido no limite de mancha zero e um número infinito de k-pontos.  Com base nisso, decida quais valores de nk1 = nk2 = nk3 e degauss que você considera satisfatórios.

### Tarefa 2: Bulk Modulus
Altere os valores de degauss e K_POINTS  obtidos no cálculo da convergência do exercício 1  no input `Al.sc`

**2.1.** Obtenha a constante de rede de equilíbrio do Al:
Proceda como fez para Si, procure uma constante de rede que esteja no intervalo de 7.0 a 8.0 bohr  variando 0.1 e edite o arquivo `bulk_modulus_Al.dat`.

**2.2**  Faça o gráfico de energia verus constante de rede. Qual é o valor da constante de rede? Compare com trabalhos experimentais da literatura.

### Tarefa 3: Estrutura de Bandas do Alumínio

**3.1**  Abra  o diretório  Al /Bands
Você verá os seguintes arquivos:

**Al.scf.in** este é um modelo de input para uma célula Al primitiva.
**Al.nscf.in** este é um modelo de input para realizar cálculos não consistentes. 
**Al.dos.in**, este é um modelo de input para realizar cálculos de densidade de estados.
**Al.bands.in** este é um modelo de input para  gerar a estrutura de bandas.
 **k-point-path** este é um arquivo que contém uma lista de k-points ao longo de direções de simetria na zona de Brillouin.
**Al.plotband.in** este é um arquivo de entrada para colocar os dados da estrutura da banda em um formato plotável.

**3.2** Abra e leia o arquivo de amostra  `Al.scf.in`
Altere os valores de degauss e K_POINTS  obtidos no cálculo da convergência do exercício 1 

**3.3** Execute um cálculo scf:

```bash
$ pw.x <Al.sample.in> Al.sample.out
```

**4** Cálculos não autoconsistentes (nsfc):
**4.1** Abra o arquivo Al.nscf.in 
**4.2** Observe as diferenças entre scf para nscf 
  **4.2.1**   o cálculo do sinalizador = 'nscf'
   **4.2.2** occupations='tetrahedra' in the namelist &SYSTEM.
 ** 4.2.3**  K_POINTS card is hanged from “6 6 6 1 1 1” to “12 12 12 1 1 1”, isso porque agora queremos calcular os valores próprios em uma malha mais fina no espaço k.
  
Lembre-se de que as mesmas funções de onda (conforme obtidas nos cálculos de scf) devem ser usadas, então o MESMO prefixo dos cálculos de scf !

**4.3** Execute os cálculos nscf: 

$pw.x <Al.nscf.in> Al.nscf.out
 
**5** Cálculos DOS para o Al:

Abra o input Al.dos.in
**5.1** Certifique-se de que tem o mesmo prefixo usado nos cálculos de scf.
**5.2** Verifique a faixa de energia dos valores próprios obtidos no arquivo de saída nscf Si.nscf.out. Emin e Emax fornecem esse intervalo. 
**5.3** Os resultados do DOS são escritos em fildos = dos.dat
**5.4** Execute cálculos de densidade de estados
 $  dos.x <Al.dos.in> Al.dos.out
 
**5.5** Dê uma olhada em dos.out e o arquivo de dados Al.dos.dat .
**5.6** Plote dos.dat para ver o gráfico do DOS (você pode usar os programas gnuplot ou xmgrace ).

**6** Cálculos da estrutura de banda para Al
**6.1** Siga o mesmo procedimento que foi usado para o exemplo de Si. (Os arquivos de entrada para Al são fornecidos nesta pasta.)
**6.2** Escreva as diferenças entre a estrutura de bandas do Si e do Al.


## Sistema 3: Homodímeros de Metanol

Nesta prática iremos calcular através da computação voluntária a energia de interação entre os homodímeros do metanol, através de algumas configurações. O objetivo dessa prática é obter um conjunto de dados para criar um campo de força via Machine Learning para o metanol. Depois de obter o campo de força, iremos implementar esse sistema em um cálculo de dinâmica molecular para o bulk de metanol.

* Calcule quatro pontos para  a energia de interação entre os homodímeros para cada configuração. Obs: São quatro configurações!

Na pasta  `lab6/Metanol` é possível encontrar quatro pastas: conf1, conf2, conf3, e conf4. Dentro dessas pastas temos outros diretórios  r1, r2,..., r24. 


**1.** Primeiro entre no diretório `lab6/Metanol/conf1` e  calcule o ponto escolhido pra você no arquivo (através do número USP)
https://docs.google.com/document/d/1gSY29GHpGXS6kiEKzpyWHJpTDBXt0j93eBJ71_zf-Vo/edit

**2.** Entre no diretório determinado através do seu número usp.

**3.1** Execute o cálculo, porém antes de executar o cálculo, leia as observações:

```bash
$ pw.x <confrXXX.in> confrXXX.out 
```

* Obs: Aqui você vai substituir rXXXX por r1, r2, r3... é muito importante seguir esse padrão, por exemplo para o ponto r10 

```bash
$ pw.x <confr10.in> confr10.out 
```

**3.2** Informe o valor da energia para cada ponto calculado no arquivo docs:
https://docs.google.com/document/d/1gSY29GHpGXS6kiEKzpyWHJpTDBXt0j93eBJ71_zf-Vo/edit
* Note que no arquivo do docs tem quatro configurações diferentes para o metanol.

**3.3** Agora, repita o processo para as configurações 2, 3 e 4.

**4** Calcule a energia de interação (E), calculada pela fórmula:
 E = E1 - 2(E2),
 
* onde E1 é a energia entre os dímeros obtida no cálculo processo 3 e E2 é a energia da molécula isolada, calculada na tarefa zero.

**5** Plote o gráfico da energia de interação versus distância para cada configuração. 

**6** Responda: Quais são  as configurações mais atrativas? 
