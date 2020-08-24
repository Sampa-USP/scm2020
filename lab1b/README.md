# Aprendendo Git

## Introdução

**Git** é um sistema de controle de versões (*VCS, version control system*). Ele pode ser utilizado para gerenciar alterações em um simples arquivo de texto, mas ganhou notoriedade no desenvolvimento de software *opensource*. O servidor mais conhecido de projetos gerenciados com **git** na web é o **GitHub**. 

Obs: **GitHub** é apenas um servidor para diretórios gerenciados via **git** (e não é o único). É possível utilzar **git** sem ter uma conta no **GitHub**.

No **git** os dados são estruturados como: 
- Diretórios (*folders*) = trees
- Arquivos (*files*) = blobs
- Estados temporais = versions (*commits*)

Ou seja, adicionamos diretórios e arquivos ao sistema de versionamento, que então faz o controle mantendo *snapshots* (i.e. como fotografias de um filme) do estado atual da estrutura de diretório e conteúdo dos arquivos. Cada vez que um usuário realiza um *commit*, o **git** irá armazenar o conteúdo dos arquivos, junto de metadados contendo informações sobre aquele estado (autor, mensagem, objetos contendo o estado de cada arquivo). 

Os commits são adicionados em uma linha temporal, de modo que um histórico das mudanças nos arquivos é mantido. O conteúdo de cada snapshot é associado a uma hash (uma chave alfanumérica com os endereços de cada arquivo naquele estado) e opcionalmente uma referência (e.g. versão 1.0 do software). Conforme a necessidade, é possível comparar mudanças entre diferentes *commits* e também resgatar trechos e versões antigas.

## Comandos básicos
### Criando um diretório

Vamos criar um diretório **test** e iniciar um repositório **git** nesse diretório:

```
mkdir test
cd test
git init
git help init 
ls -a
ls .git
git status
```

No diterório oculto **.git**, é possível ver a estrutura de objetos e referências que **git** irá utilizar. **Não** altere os arquivos nesse diretório. Para o comando "git status", **git** irá retornar a mensagem "No commits yet", ou seja, nenhum snapshot foi registrado.

### Staging area (quais arquivos serão monitorados?)

Para indicar quais mudanças devem ser incluídas no próximo snapshot, vamos criar um arquivo de texto e utilizar o comando **git add**

```
echo "Detalhes do projeto: (...)" > README.MD
git status
```

O arquivo README.MD, apesar de não ser obrigatório, está presente na maioria dos repositórios **git** e contém informações sobre o projeto. Ele é escrito na linguagem de texto **markdown**, que permite de maneira simples e direta formatar textos, incluir trechos de códigos, links, comandos, figuras e tabelas. Um pouco sobre markdown pode ser visto em outras referências como, por exemplo, [nesse link](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), mas não se preocupe com isso nesse momento, trate o arquivo como um simples arquivo de texto.

O **git** irá perceber que um novo arquivo foi criado, mas se ele não for selecionado para ser gerenciado com **git add**, o **git** irá ignorá-lo.

```
git add README.MD
git status
git commit -m "Primeira versão do meu projeto (initial commit)"
git log
```

Uma primeira versão da pasta foi adicionada ao controle de versões **git**. Dica: escolha boas mensagens para os seus commits para ajudar a identificar alterações realizadas nos arquivos.

P: Por que realizar o processo em duas etapas (add & commit)? 
R: Alguns arquivos (logs) não precisam ser controlados - basta não adicioná-los (cuidado ao utilizar "git add -a"). 

Para visualizar seus *commits*, utilize o comando git log. Commits mais recentes são apresentados no topo da lista. **HEAD** indica o estado atual do diretório. Obs: observe que **HEAD** irá apontar para outra versão se for utilizado o comando **git checkout**.

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

A possibilidade de se trabalhar em diversas ramificações do código é que tornaram **git** uma ferramenta tão popular no desenvolvimento de software. Essas ramificações, também chamadas de *branches*, são em gerais criadas quando estamos corrigindo um bug, ou implementando uma nova função no código, e não queremos bagunçar o nosso ramo principal, chamado de *master*. Isso é feito pois durante o desenvolvimento em um *branch*, iremos fazer *commits* de versões que não foram completamente testadas, ou até mesmo não são completamente funcionais. 

Essa abordagem também permite que trabalhemos no ramo principal, em paralelo ao desenvolvimento de uma nova funcionalidade, por exemplo. Isso significa que podemos lançar versões do código, e ir corrigindo bugs em versões pontuais como `1.0.1`, `1.0.2`, antes de introduzir a nova funcionalidade na versão `2.0`.

Depois de completar a tarefa que estamos fazendo em um determinado **branch**, podemos levar as mudanças novamente ao ramo principal. Isso é feito através de um processo chamado **merge**. Durante esse processo, todo o histórico de mudanças durante do desenvolvimento é mantido. 

A figura abaixo ilustra bem a estrutura de *commits* quando se utiliza *branches*. Vemos que a linha do tempo não é mais somente linear. Na figura, o *branch* `iss53` se desprende do ramo `master` no commit `C2`. Fazemos então um implementação no ramo `iss53`, gerando o *commit* `C3`. Após isso, resolvemos um bug simples no ramo `master` e fazemos o *commit* `C4` antes de continuar trabalhando na nova implementação e gerar o *commit* `C5` no ramo `iss53`. Em `C6`, fazemos o **merge** e um *commit* de *merge* é adicionado, onde a implementação que estava em no *branch* `iss53` é agora levada ao ramo principal.

![historico commits](https://git-scm.com/book/en/v2/images/basic-merging-2.png)

Para criar um ramo (**branch**) independente de nosso código, usaremos o comando **git branch**. 

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

### Usando outras funcionalidades do GitHub
Além de servir como servidor para repositórios **git**, o GitHub possui outras funcionalidades.
Por exemplo, todo repositório **git** no GitHub conta com um **issue tracker**, que pode ser utilizado por usuários e desenvolvedores para acompanhar e reportar bugs e/ou requisitar novas funcionalidades.

O caráter colaborativo do GitHub também fica claro devido aos **pull requests**.
Os *pull requests* são sugestões de *commits* que outros usuários que não são necessariamente desenvolvedores naquele projeto podem fazer.
Além disso, é possível utilizar no GitHub ferramentas para teste automático, coordenar o projeto com painéis parecidos como no Trello, e uma variedadade de outras facilidades.
Essas funcionalidades fogem do escopo desse tutorial, contudo, são importantes espcialmente para projetos grandes e complexos.

### Comandos adicionais

Se você pretende utilizar **git** em seus projetos, procure por mais informações sobre os comandos:

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


