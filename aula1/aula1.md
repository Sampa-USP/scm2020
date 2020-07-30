# Simulação Computacional dos Materiais - IFUSP
# Aula 1 - Linux e Bash/Shell

## 1) Os comandos principais:

Navegação: 
- **ls (list)**
- **cd (change directory)**
- **pwd (print work directory)**
- **clear**

Exemplo de código:

```bash
> ls
> cd ~/
> pwd
> ls -l
> cd /home/
> clear 
```

Gerenciando arquivos: 
- **mkdir (make directory)**
- **touch**
- **mv (move)**
- **rm (remove)** 
- **cp (copy)**
- **cat (concatenate)**
- **head**
- **tail**
- **comm, cmp (compare)**
- **grep**

Exemplo de código:

```bash
> mkdir teste
> touch teste.txt
> mv teste.txt teste2.txt
> mv ../teste2.txt
> cd ../
> cp teste2.txt teste
> cd teste 
> head teste2.txt
> tail teste2.txt
> touch teste1.txt
> cmp teste1.txt teste2.txt
> grep 'fim' teste2.txt
```

Processos: 
- **ps (process status), top** 
- **kill**
- **which**
- **source**
- **wget** 
- **chmod**
- **echo**
- **tar**
- **wc (word count)**
- **man CMD (manual)**
- **apt-get update/updgrade/install**
- **python**

## 2) Aplicação: 

- Gerenciando trabalhos (usando *while*): 
```bash
#!/bin/bash
if ! [ -e list.txt ]; then
  echo "Could not find a list.txt"
  echo "STOP"
  exit
fi

while read i; do
  if [ -e ../$i/01.out ]
    then
      echo $i
    else
      source job.sh
      sleep 10
      echo $i
  fi
done <list.txt
```

- Gerenciando trabalhos (usando *for*): 
```bash
#!/bin/bash
n=100
for i in `seq -f "%03g" $n`
do
  cd $i
    if [ -e 01.out ]
    then
      echo $i		
    else
      source job.sh
      sleep 10
      echo $i
    fi
  cd ..
done

python python_script.py
```

- Gerenciando trabalhos no terminal:
```bash
#!/bin/bash
source ./env.sh
    # export PATH=""
nohup command <input 1> out.log 2>&1 &
echo $! > save_pid.txt
```

- Usando *grep* (com um arquivo do Quantum-espresso):
```bash
grep 'total energy' 01.out
  > total energy = -517.95883538 Ry
  > total energy = -516.95645343 Ry
  > total energy = -519.28686151 Ry
  > total energy = -520.00138545 Ry
  > total energy = -520.24540354 Ry
  > total energy = -520.16628398 Ry
  > The total energy is the sum of the following terms:
```

-Usando *wc* 
```bash
wc -l iter.000000/02.fp/*out
  > 557 iter.000000/02.fp/candidate.shuffled.000.out
  > 453 iter.000000/02.fp/rest_accurate.shuffled.000.out
  >   0 iter.000000/02.fp/rest_failed.shuffled.000.out
  > 1010 total
```

Comandos especiais (operadores, modificadores, etc): 
- **nice** 
- **nohup**
- **mpirun**
- **>, |, &**

```bash
nohup process input 1> out.log 2>&1 &
```

## 3) Gráficos com gnuplot:

- Gerenciando trabalhos (usando *while*): 
```bash
tail -f file.out
  > ultima linha escrita no arquivo (...)
  > (Ctrl+C para sair)

gnuplot
  > set terminal dumb			# graficos no terminal
  > set title ""
  > set xrange [-1:1]
  > set zeroaxis
  > set logscale
  > p 'file.out' 1:4 			# a partir de um arquivo 
  > p (x/4)**2, sin(x), 1/x
```

# Dúvidas

https://stackoverflow.com/
