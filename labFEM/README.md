# Cálculos de elementos finitos utilizando o Elmer

Neste tutorial, vamos aprender a fazer a simulação de uma perna protética utilizando o método dos elementos finitos (FEM). O arquivo de entrada que será utilizado nas simulações pode ser obtido [aqui](./Cheetah.stp).

Iremos utilizar o software [Elmer](http://www.elmerfem.org/blog/), um programa de código aberto muito bem documentado.

## Ajustes na máquina virtual

No terminal, tente abrir o software com o comando **ElmerGUI**. Caso o sistema acuse a ausência da biblioteca **libQt5Xml.so.5**, favor re-instalar com o comando:

```bash
sudo apt-get install libqt5xml5
```

## Tutorial

Agora basta seguir o tutorial em vídeo que pode ser encontrado no link: [video](http://www.youtube.com/user/elmerfem)