# Introdução a campos de força e ao LAMMPS

Conforme apresentado em aula, a dinâmica molecular clássica é realizada com potenciais de mecânica molecular.
Esses potenciais, chamados de campos de força, descrevem as interações entre os átomos do sistema.

Para entender melhor o funcionamento dos campos de força vamos realizar o cálculo de energia e minimização de energia no LAMMPS.
O LAMMPS, assim como outros programas que realizam dinâmica molecular, lê as coordenadas dos átomos e os parâmetros do campo de força de um arquivo de texto, que é usualmente chamado de **topologia**.

## Objetivo

- Entender a estrutura básica do arquivo de topologia do LAMMPS
- Entender a estrutura básica do arquivo de entrada do LAMMPS
- Realizar a minimização de energia de diferentes moléculas

## Otimização da molécula de metano no campo de força OPLS-AA

![metano](imgs/metano_comb.png)

## Otimização da molécula de etanol no campo de força OPLS-AA

![etanol](imgs/EtOH_comb.png)

## Otimização de um peptídeo 5-mer descrito com o CHARMM

![peptideo](imgs/peptide.png)