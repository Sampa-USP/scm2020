# Simulação Computacional dos Materiais - IFUSP
# Aula 1 - Linux e Bash/Shell

Shell é um ambiente baseado em texto - ou interface de linha de comando - que permite armazenamento de variáveis, gerenciamento de diretórios e arquivos e execução de programas. Bash é o programa shell presente em sistemas operacionais base GNU (Linux e MacOS). Como Bash possuí um interpretador dos comandos realizados no shell, bash pode ser considerada uma linguagem de programação. 

## 0) Antes de começar...

Para garantir uma funcionalidade completa da VM, você vai precisar instalar o **VirtualBox Guest Additions**. Baixe o setup [aqui](https://download.virtualbox.org/virtualbox/6.1.12/Oracle_VM_VirtualBox_Extension_Pack-6.1.12.vbox-extpack).

Alternativamente, no caso de Linux, siga as instruções abaixo:
```bash
sudo apt update
sudo apt upgrade
sudo apt install build-essential dkms linux-headers-$(uname -r)
```

Inicie a sua máquina virtual utilizando o VirtualBox. Lembre-se, as senhas de acesso são "scm2020" (máquina Ubuntu "full") e "stds9" (máquina Lubuntu "lite"). Você pode alterar as senhas da sua VM se quiser. Para iniciar o terminal, use o atalho Ctrl+Alt+T.

**Configurações adicionais**

A) Caso seja necessário reinstalar o Guest additions na VM: 

Vá em **Devices > Insert Guest Additions CD** e execute o comando autorun.sh. Isso irá instalar o Guest additions na VM.

B) Para criar um diretório a ser compartilhado com a VM:

- No seu sistema operacional base: criar uma pasta compartilhada, ex: **shared**. Máquinas linnux devem habilitar a leitura e escrita na pasta desejada automaticamente. **Caso você esteja utilizando Windows:**

- No Windows, clique direito > propriedades > compartilhamento > compartilhar > permitir leitura/escrita de qualquer usuário.
- Na aba avançado > habilite a opção "Compartilhar essa pasta".

C) **Problemas com o teclado?**
A VM está configurada para um teclado PT-BR com tecla **Ç**. Para alterar, na VM:
- Clique direito na barra inferior
- Add / Remove Panel Items, Add
- Keyboard Layout Handler

Agora você pode alterar o teclado no canto inferior direito (bandeira do Brasil, ao lado do relógio). 


## 1) Os comandos principais:

Navegação: 
- **ls (list)**
- **cd (change directory)**
- **pwd (print work directory)**
- **clear**

Exemplo de código:

```bash
echo Texto
echo $PATH
which echo
vim ~/.bashrc
# Para sair do vim, pressione Ctlr+C, :qa!, enter.
ls
cd ~/
```

Gerenciando arquivos e extraindo informações: 
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
mkdir teste
touch teste.txt
mv teste.txt teste2.txt
mv ../teste2.txt
cd ../
cp teste2.txt teste
cd teste 
head teste2.txt
tail teste2.txt
touch teste1.txt
cmp teste1.txt teste2.txt
grep 'fim' teste2.txt
rm test1.txt
```

ATENÇÃO: 'rm' garante uma remoção permanente do arquivo. Use com cuidado, pois uma vez que o arquivo for removido, as chances de recuperá-lo são pequenas. 

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

- É possível utilizar diversos operadores para combinar parâmetros
- **>, |, &**

```bash
echo mensagem > msg.txt
cat msg.txt
cat < msg.txt > msg2.txt
cat msg2.txt 
cat < msg.txt >> msg2.txt
cat msg2.txt
ls -l | tail -1
ls -l | tail -1 > lastfile.txt
```

- Criando pastas e gerenciando trabalhos (usando *while*): 
```bash
#!/bin/bash
#Criando pastas com base em uma lista (list.txt)

if ! [ -e list.txt ]; then
  echo "Could not find a list.txt"
  echo "STOP"
  exit
fi

while read i; do
  mkdir $i
done <list.txt
```

```bash
#!/bin/bash
#Criando arquivos nas pastas

if ! [ -e list.txt ]; then
  echo "Could not find a list.txt"
  echo "STOP"
  exit
fi

while read i; do
  cd $i
  if [ -e 01.out ]
    then
      echo $i
    else
      echo 'Output file' > 01.out
      sleep 5
      echo $i
  fi
  cd ../
done <list.txt
```

- Gerenciando trabalhos (usando *for*): 
```bash
#!/bin/bash
n=5
for i in `seq -f "%03g" $n`
do
  cd $i
    if [ -e 01.out ]
    then
      echo $i		
    else
      source job.sh
      python python_script.py
      sleep 10
      echo $i
    fi
  cd ..
done
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
wc -l job/*out
  > 557 iter.000000/02.fp/candidate.shuffled.000.out
  > 453 iter.000000/02.fp/rest_accurate.shuffled.000.out
  >   0 iter.000000/02.fp/rest_failed.shuffled.000.out
  > 1010 total
```

Comandos (programas) especiais: 
- **nice** 
- **nohup**
- **mpirun**

```bash
nohup process input 1> out.log 2>&1 &
```

## 3) Visualização de arquivos; gráficos com gnuplot:

- Gerenciando trabalhos (usando *tail -f*): 
```bash
tail -f file.out
    # ultima linha escrita no arquivo (...) - real time
    # (Ctrl+C para sair)

xcrysden --pwi 01.in

gnuplot
    set terminal dumb # graficos no terminal
    set title ""
    set xrange [-1:1]
    set zeroaxis
    set logscale
    plot 'file.out' using 1:4 with lines # a partir de um arquivo
    p 'file.out' u 1:4 w l
    p (x/4)**2, sin(x), 1/x
    set key outside
    plot for [col=1:4] 'file.out' using 0:col with lines
```

# Dúvidas

https://stackoverflow.com/