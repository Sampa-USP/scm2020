# Introdução à dinâmica molecular com o LAMMPS

A dinâmica molecular (DM) é uma técnica de simulação molecular que integra as equações de movimento de sistemas atômicos e moleculares para simular o sistema de interesse nas condições termodinâmicas desejadas.
Neste tutorial, estamos interessados em introduzir a DM utilizando **campos de força** clássicos, que mimetizam as interações entre as partículas utilizando expressões analíticas para a energia potencial. 
Essas expressões possuem **parâmetros** que devem ser escolhidos de maneira adequada para o sistema de interesse.
Esses parâmetros, por sua vez, são otimizados para reproduzir propriedades microscópicas (como estrutura, obtida com cálculos *ab initio* ou com raios x/NMR) e macroscópicas do sistema (como a densidade).
Para um mesmo sistema, mais de uma parametrização pode existir, e um ou outra pode ser mais adequada a depender da propriedade que se deseja analizar e das condições termodinâmicas.

Para realizar a simulação de DM, utilizaremos o software [LAMMPS](https://lammps.sandia.gov/), que tem o seu nome baseado no acrônimo Large-scale Atomic/Molecular Massively Parallel Simulator.

## Objetivos

Neste tutorial temos como objetivo introduzir os conceitos básicos de DM no LAMMPS. Vamos abordar:
- Criação de topologia de uma configuração
- Arquivos de entrada do LAMMPS
- Minimização de energia
- Simulação no ensemble natural da DM (*NVE*)
- Simulação no ensemble típico de experimentos (*NPT*)
- Cálculo de propriedades de interesse em uma simulação de água

## Estrutura dos arquivos de entrada para o LAMMPS

Para executar o LAMMPS é necessário criar um arquivo de entrada (arquivo de texto, geralmente iniciado por `in.` ou terminado por `.in`) que contém informações sobre a simulação, como temperatura, **time step**, *ensemble* simulado, frequência da escrita das propriedades calculadas etc.
Esse mesmo arquivo pode ser utilizado para se construir a **topologia** do sistema, que contém a forma e dimensões da **caixa de simulação**, as coordenadas atômicas, e parâmetros do campo de força. 
Contudo, para sistemas mais complexos a topologia normalmente é especificada em um outro arquivo, que é incluido no arquivo de entrada principal `in` utilizando o comando `read_data`.

## Criando uma caixa de simulação com diversas moléculas de água

Desejamos realizar simulações de dinâmica molecular da água na fase *bulk* a 300K e 1atm.  Um bom ponto de partida é criar uma configuração molecular que possui a densidade experimental da água nessas condições (1.0 g/cm<sup>3</sup>).

Usaremos o pacote [PACKMOL](http://m3g.iqm.unicamp.br/packmol/home.shtml) para gerar uma configuração inicial  contendo 267 moléculas em uma  caixa de volume  8.0 nm<sup>3</sup>. 

Primeiro, vamos instalar uma dependência que está faltante na VM, e que faz com que os binários não funcionem:
```bash
sudo apt install libgfortran3
```
Lembre que a senha da VM é `stds9`. Pressione `Enter` para aceitar a instalação dos novos pacotes e continuar a instalação.

Instalada a dependência, vamos criar agora a caixa de simulação com a densidade da água.
O arquivo `water.inp` contém os comandos de entrada para o PACKMOL, abra e tente entender o seu conteúdo (os comentários após os `#` devem auxiliar).
Para gerar a configuração, execute  o seguinte comando no diretório `criar_topol`:

```bash
./packmol < water.inp
```

Podemos visualizar a configuração gerada com o programa *Visual Molecular Dynamics* (VMD):

```bash
vmd bulk_water.xyz
```

A partir do arquivo `bulk_water.xyz` podemos gerar o arquivo de  topologia do sistema que deverá conter informações essenciais sobre o campo de força utilizado. Esse arquivo contém os parâmetros   Lennard-Jones e as cargas do potencial de Coulomb, entre outros dados. O arquivo de topologia pode ser gerado através do *script* `topol.sh`:

```bash
./topol.sh
```

O arquivo `bulk_water.top` é  gerado replicando as informações sobre uma única molecula contidas no documento `water.top`. Abra-os para visualizar e entender a sua estrutura.

## Simulação no ensemble *NVE*

Execute a seguinte linha de comando para realizar a simulação no ensemble microcanônico:

```bash
mpirun -np 2 lammps < in.water_nve
```

O `mpirun -np 2` antes do comando `lammps` indica que o programa deve ser executado usando 2 processadores em **paralelo**.
Remova-o caso sua máquina virtual esteja configurada com apenas um processador, o resultado deve ser o mesmo, somente o tempo de execução deve mudar.

Após alguns minutos (de 2 a 10), os seguintes arquivos serão gerados:
- `log.lammps`: arquivo com informações da simulação
- `bulk_water.lammpstrj`: arquivo das trajetórias
- `prod_bulk_water.top`: arquivo de topologia que poderá ser utilizado em uma próxima simulação.

Vamos agora fazer o gráfico de algumas propriedades.
Para isso, vamos utilizar o *script* `lammps_plotter.py` que está no diretório `utils`.
Para fazer gráficos utilizando o *script* utilize comandos como o abaixo:
```bash
./utils/lammps_plotter.py log.lammps 1 2 --ignore-optimization --multx-timestep
```
sendo o primeiro argumento o arquivo com o `log` da simulação, o segundo argumento a coluna do eixo `x` do gráfico (nesse caso `1` indica `Step` - visualize o arquivo `log.lammps` para ver o significado de cada coluna) e o terceiro argumento o eixo `y`.
Com o comando acima você fará um gráfico da evolução da temperatura (coluna `2`) com o tempo (pois utilizamos a opção `--multx-timestep`).
A opção `--ignore-optimization` serve para não graficar a saída do comando `minimize`.

Faça gráficos da temperatura, energia cinética, energia potencial, energia total e pressão.
Essa simulação chegou ao equilíbrio?