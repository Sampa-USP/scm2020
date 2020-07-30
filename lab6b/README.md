# Simulação Computacional dos Materiais - IFUSP
## Aula Lab6b - Cálculos de DFT em lotes (batches)

Nesta aula, trabalharemos com compostos intermetálicos Nb(x)-Fe(y). Escolha uma das pastas disponibilizadas em [jobs](./jobs). Cada pasta contém 20 estruturas com a mesma estequiometria; em cada estrutura (00001-00020), as posições atômicas foram deslocadas em até 0.2 angstrons das posições de equilíbrio, de maneira aleatória. Deste modo, cada estrutura é única e levará a resultados distintos.

Observação: a pasta PP será utilizada por todos os grupos; ela contém pseudopotenciais do tipo PAW-PBE utilizados nos cálculos.

### 1) Cálculos isolados:

- Depois de ter escolhido o seu diretório de trabalho, entre na pasta 00001 e verifique o arquivo 01.in. Trata-se de um arquivo de input do quantum-espresso. Para mais informações, acesse [a documentação do código pw.x](https://www.quantum-espresso.org/Doc/INPUT_PW.html).

- Em resumo, o arquivo 01.in está definindo parâmetros de controle, sistema, configuração eletrônica, critérios de convergência, estrutura cristalina e cada uma das posições atômicas dos átomos presentes na estrutura, respectivamente. 

- Esses arquivos foram preparados de maneira que cada cálculo possa ser realizado em menos de 10 min em uma máquina x64 atual. Parâmetros que influenciam massivamente no tempo computacional são os critérios de convergência de energia, de força e a matriz de K_POINTS.

- Para visualizar a estrutura 1/20 utilizando o **xcrystden**, digitar:
```bash
cd 00001
xcrysden --pwi 01.in
```
- Outra opção é utilizar softwares com interface gráfica como o VESTA. **Dica: Sempre visualize as estruturas antes de alocar recursos computacionais para cálculos de DFT**. 

- Antes de iniciar os cálculos em série, vamos tentar realizar um cálculo isolado, para ter certeza de que não há nenhum problema com o arquivo de input. Voltando ao terminal, para iniciar o cálculo digite:
```bash
mpirun -n 2 pw.x < 01.in > 01.out
```

- Abra um segundo terminal para acompanhar a execução do código *on-the-fly*:
```bash
tail -f 01.out
```
- Finalizado o cálculo, verifique quantas iterações foram necessários para atingir a convergência, e também as forças finais observadas em cada átomo.

### 2) Cálculos em lote

- Agora já sabemos que os arquivos de input estão funcionado bem. 

- Abra o arquivo 01.in na pasta 00002 e compare as posições atômicas com o primeiro arquivo (da pasta 00001). Você verá que elas são similares, mas não idênticas. Certidique-se de que as posições atômicas são as únicas diferenças entre um arquivo e outro.

- É hora de preparar os *scripts* para execução dos trabalhos em série. 

- Volte ao seu diretório de trabalho e inspecione os arquivos *copy_job.sh* e *submit_jobs.sh*. O primeiro é um simples script em bash para copiar o arquivo *job.sh* em cada uma das pastas (00001-00020). O segundo permite a execução em série de cada *job.sh*, com um intervalo de 15s entre os trabalhos. Ajuste o arquivo *job.sh* conforme as necessidades da sua máquina e, após, execute os scripts:

 ```bash
./copy_job.sh
./submit_jobs.sh
```
- Você pode monitorar a execução dos trabalhos via terminal, utilizando o comando **grep**. Também é possível verificar detalhes da execução, monitorando os arquivos 01.out relativo ao último trabalho iniciado.

- Depois de realizados os cálculos, verifique a energia final de cada variante. Qual das estruturas apresentou a menor energia? E a maior? 

## Agradecimentos
