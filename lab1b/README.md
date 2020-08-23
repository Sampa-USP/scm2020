# Aprendendo Git

## Introdução

**Git** é um sistema de controle de versões (*VCS, version control system*). Ele pode ser utilizado para gerenciar alterações em um simples arquivo de texto, mas ganhou notoriedade no desenvolvimento de software *opensource*. A versão mais conhecida do **git** na web é conhecido como **GitHub**. 

Obs: **GitHub** é apenas um servidor para diretórios gerenciados via **git** (e não é o único). É possível utilzar **git** sem ter uma conta no **GitHub**.

Estrutura dos dados: 
- Diretórios (*folders*) = trees
- Arquivos (*files*) = blobs
- Estados temporais = versions (*commits*)

Cada vez que um usuário realiza um *commit*, **git** irá armazenar os arquivos agrupados em *snapshots* (i.e. como fotografias de um filme), junto de metadados contendo informações sobre aquele estado (autor, mensagem, objetos contendo o estado de cada arquivo). Commits são adicionados na linha temporal. O conteúdo de cada snapshot é associado a uma hash (uma chave alfanumérica com os endereços de cada arquivo naquele estado) e uma referência (e.g. versão de teste).

## Comandos básicos
### Criando um diretório

Vamos criar um diretório **test** e iniciar **git** nesse diretório:

```
mkdir test
cd test
git init
git help init 
ls -a
ls .git
git status
```

No diterório oculto **.git**, é possível ver a estrutura de objetos e referências que **git** irá utilizar. Não altere os arquivos nesse diretório. Para o comando "git status", **git** irá retornar a mensagem "No commits yet", ou seja, nenhum snapshot foi registrado.

### Staging area (quais arquivos serão monitorados?)

Para indicar quais mudanças devem ser incluídas no próximo snapshot, vamos criar um arquivo de texto e utilizar o comando **git add**

```
echo "Detalhes do projeto: (...)" > README.MD
git status
```

**Git** irá indicar que um novo arquivo foi criado, mas se ele não for selecionado com **git add**, **git** irá ignorá-lo.

```
git add README.MD
git status
git commit -m "Primeira versão do meu projeto (initial commit)"
git log
```

Uma primeira versão da pasta foi adicionada ao controle de versões **git**. Dica: escolha boas mensagens para os seus commits para ajudar a identificar alterações realizadas nos arquivos. 
P: Por que realizar o processo em duas etapas (add & commit)? 
R: Alguns arquivos (logs) não precisam ser controlados - basta não adicioná-los (cuidado ao utilizar "git add -a"). 


Para visualizar sua tree, utilize o comando git log. Commits mais recentes são apresentados no topo da lista. **HEAD** indica o estado atual do diretório. Obs: observe que **HEAD** irá apontar para outra versão se for utilizado o comando **git checkout**.

```
git log --all --graph --decorate
```

### Versões antigas

Utilizando o comando **git checkout <hash>** você pode restaurar versões antigas. Cuidado ao alterar arquivos em versões antigas.

Com o comando **git diff** é possível observar alterações realizadas em arquivos (ou versões) específicas.

```
git diff <commit> HEAD README.MD
cat README.MD
```

### Branch and merge (ramificações do código)

A possibilidade de se trabalhar em diversas ramificações do código é que tornaram **git** uma ferramenta tão popular no desenvolvimento de software. Para criar um ramo (**branch**) independente de nosso código, usaremos o comando **git branch**. 

Primeiramente, vamos criar um programa inicial com python:

```
vim salve.py 

# --start
import sys

def default():
    print('o que voce quer?')

def main():
    default()

if __name__ == '__main__':
    main()
# --end

git status
git add salve.py
git commit
git log 
```
Teste o programa com python salve.py. Ele já foi incluído no controle de versões **git**. Agora vamos implementar outras opções de resposta em um novo *branch* (klingon):

```
git branch -vv
git branch klingon
git log
git checkout klingon
git log

vim salve.py 

# --start
import sys

def klingon():  #add
    print('nuqneH')  #add

def default():
    print('o que voce quer?')

def main():
    if sys.argv[1] == 'klingon':  #add
       klingon()  #add
    else:
       default()

if __name__ == '__main__':
    main()
# --end

git status 
git diff
git add salve.py 
git commit
git log --all --graph --decorate
```

A função klingon() só foi implementada no ramo klingon. Isso quer dizer que se restaurarmos a versão original (git checkout master), não teremos a função implementada em salve.py. Mas e se houver mais de 1 ramo de desenvolvimento ativo, sendo modificado paralelamente?

Vamos criar um outro branch, a partir do código original, independente do ramo klingon(). Para tal:

```
git checkout master
git checkout -b volcano
git log

vim salve.py 

# --start
import sys

def klingon():  #add
    print('dif-tor heh smusma')  #add

def default():
    print('o que voce quer?')

def main():
    if sys.argv[1] == 'volcano':  #add
       volcano()  #add
    else:
       default()

if __name__ == '__main__':
    main()
# --end

git status 
git diff
git add salve.py 
git commit -m 'Volcanos encontrados'
git log --all --graph --decorate --oneline
```

Ok. Temos três ramos de desenvolvimento distintos. Chegou o momento de unir os esforços de humanos, klingons e volcanos em um único código utilizando o comando **git merge**:

```
git checkout master
git merge klingon
```

Aparentemente, a primeira união (merge) ocorreu sem problemas, e a função klingon() foi incorporada em master. 

```
git merge volcano
git merge --abort
```

Entretanto, como o ramo volcano partiu de um estado anterior ao atual, **git** está indicando um conflito ao tentar realizar a união. Vamos identificar e resolver esse conflito manualmente:

```
git merge volcano
vim salve.py

# --
def main():
    if sys.argv[1] == 'klingon':
       klingon()
    elif sys.argv[1] == 'volcano':	#modified
       volcano()
    else:
       default()
# --

git merge --continue
```

Agora o código salve.py tem ambas as funções (klingon e volcano) implementadas.

## Git online
### Git remote (colaborando com outras pessoas online)

Se você quer colaborar com outras pessoas, está na hora de enviar seu repositório local para um servidor remoto utilizando **git remote**.

```
git remote add origin <url>
git push -u origin master
git log --all --graph --decorate --oneline
```

Para iniciar um repositório a partir de um repositório do Github, utilize o comando **git clone**. Para baixar alterações que foram realizadas online, utilize o comando **git fetch**. O comando **git pull** é na verdade uma combinação de fetch + merge. 

### Comandos adicionais

Se vocẽ pretende utilizar **git** em seus projetos, procure por mais informações sobre os comandos:

- **git config** ou vim /.gitconfig
- **git clone --shallow** 
- **git add -p file**
- **git diff --cached**
- **git blame**
- **git stash** / **git stash pop**
- **git bisect**
- **vim .gitignore**


## Agradecimentos

Essa aula foi baseada no seguinte conteúdo:
- CS-MIT 2020: https://missing.csail.mit.edu/2020/version-control/
- Missing Semester (youtube): https://www.youtube.com/watch?v=2sjqTHE0zok&t=146s


