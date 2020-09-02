# Introdução à dinâmica molecular com o LAMMPS

A dinâmica molecular (DM) é uma técnica de simulação molecular que integra as equações de movimento de sistemas atômicos e moleculares para simular o sistema de interesse nas condições termodinâmicas desejadas.
Neste tutorial, estamos interessados em introduzir a DM utilizando **campos de força** clássicos, que mimetizam as interações entre as partículas utilizando expressões analíticas para a energia potencial. 
Essas expressões possuem **parâmetros** que devem ser escolhidos de maneira adequada para o sistema de interesse.
Esses parâmetros, por sua vez, são otimizados para reproduzir propriedades microscópicas (como estrutura, obtida com cálculos *ab initio* ou com raios x/NMR) e macroscópicas do sistema (como a densidade).
Para um mesmo sistema, mais de uma parametrização pode existir, e um ou outra pode ser mais adequada a depender da propriedade que se deseja analizar e das condições termodinâmicas.

Para realizar a simulação de DM, utilizaremos o software [LAMMPS](https://lammps.sandia.gov/), que tem o seu nome baseado no acrônimo Large-scale Atomic/Molecular Massively Parallel Simulator.

## Estrutura dos arquivos de entrada para o LAMMPS

Para executar o LAMMPS é necessário criar um arquivo de entrada (arquivo de texto, geralmente iniciado por `in.` ou terminado por `.in`) que contém informações sobre a simulação, como temperatura, **time step**, *ensemble* simulado, frequência da escrita das propriedades calculadas etc.
Esse mesmo arquivo pode ser utilizado para se construir a **topologia** do sistema, que contém a forma e dimensões da **caixa de simulação**, as coordenadas atômicas, e parâmetros do campo de força. 
Contudo, para sistemas mais complexos a topologia normalmente é especificada em um outro arquivo, que é incluido no arquivo de entrada principal `in` utilizando o comando `read_data`.

## Objetivos

Neste tutorial temos como objetivo introduzir os conceitos básicos de DM no LAMMPS. Vamos abordar:
- Criação de topologia de uma configuração
- Arquivos de entrada do LAMMPS
- Minimização de energia
- Simulação no ensemble natural da DM (*NVE*)
- Simulação no ensemble típico de experimentos (*NPT*)
- Cálculo de propriedades de interesse em uma simulação de água