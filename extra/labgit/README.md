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

## Instalando e configurando o git

Antes de iniciar o tutorial, caso você nunca tenha usado e configurado o **git**, verifique se o mesmo está instalado em sua máquina digitando:

```bash
git --version
```

Se o comando retornar a versão do **git** como, por exemplo, `git version 2.28.0` significa que o git está instalado.
Se ele não estiver instalado, antes de prosseguir com o tutorial faça a instalação de acordo com o seu sistema operacional.
Um tutorial de instalação para diversos sistemas pode ser encontrado no [Pro Git Book](https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)
Para sistemas baseados no Debian (como o Ubuntu, por exemplo) basta instalar com:

```bash
apt install git
```

Com o **git** instalado, precisamos configurar o seu nome e email, caso nunca tenha o feito.
Isso pode ser feito com os dois comandos abaixo:

```bash
git config --global user.name "NOME SOBRENOME"
git config --global user.email "EMAIL@exemplo.com"
```

## Comandos básicos
### Criando um diretório

Vamos criar um diretório **test** e iniciar um repositório **git** nesse diretório:

```bash
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

```bash
echo "Detalhes do projeto" > README.MD
git status
```

O arquivo README.MD, apesar de não ser obrigatório, está presente na maioria dos repositórios **git** e contém informações sobre o projeto. Ele é escrito na linguagem de texto **markdown**, que permite de maneira simples e direta formatar textos, incluir trechos de códigos, links, comandos, figuras e tabelas. Um pouco sobre markdown pode ser visto em outras referências como, por exemplo, [nesse link](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), mas não se preocupe com isso nesse momento, trate o arquivo como um simples arquivo de texto.

O **git** irá perceber que um novo arquivo foi criado, mas se ele não for selecionado para ser gerenciado com **git add**, o **git** irá ignorá-lo.

```bash
git add README.MD
git status
git commit -m "Primeira versão do projeto (initial commit)"
git log
```

Uma primeira versão da pasta foi adicionada ao controle de versões **git**. Dica: escolha boas mensagens para os seus commits para ajudar a identificar alterações realizadas nos arquivos.

P: Por que realizar o processo em duas etapas (add & commit)? 
R: Alguns arquivos (logs) não precisam ser controlados - basta não adicioná-los (cuidado ao utilizar "git add -a"). 

Para visualizar seus *commits*, utilize o comando git log. Commits mais recentes são apresentados no topo da lista. **HEAD** indica o estado atual do diretório. Obs: observe que **HEAD** irá apontar para outra versão se for utilizado o comando **git checkout**.

```bash
git log --all --graph --decorate
```

### Versões antigas

Utilizando o comando **git checkout <hash>** você pode restaurar versões antigas. Cuidado ao alterar arquivos em versões antigas.

Com o comando **git diff** é possível observar alterações realizadas em arquivos (ou versões) específicas.

```bash
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

```bash
vim salve.py
```
```python
# --start
import sys

def default():
    print('o que voce quer?')

def main():
    if len(sys.argv) > 1:
        print(sys.argv[1])
    else:
        default()

if __name__ == '__main__':
    main()
# --end
```
```bash
git status
git add salve.py
git commit
git log 
```
Teste o programa com "python salve.py". Ele já foi incluído no controle de versões **git**. Agora vamos implementar outras opções de resposta em um novo *branch* (klingon):

```bash
git branch -vv
git branch klingon
git log
git checkout klingon
git log

vim salve.py 
```
```python
# --start
import sys

def default():
    print('o que voce quer?')

def klingon():  #add
    print('nuqneH')  #add

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'klingon':  #add
            klingon()  #add
        else:
            print (sys.argv[1])
    else:
        default()

if __name__ == '__main__':
    main()
# --end
```
```bash
git status 
git diff
git add salve.py 
git commit
git log --all --graph --decorate
```

A função klingon() só foi implementada no ramo klingon. Isso quer dizer que se restaurarmos a versão original (git checkout master), não teremos a função implementada em salve.py. Mas e se houver mais de 1 ramo de desenvolvimento ativo, sendo modificado paralelamente?

Vamos criar um outro branch, a partir do código original (*master*), independente do ramo klingon(). Nesse caso vamos utilizar o comando reduzido **git checkout -b** para criar um novo branch e ativá-lo (i.e. **HEAD** irá apontar para o branch vulcan):

```bash
git checkout master
git checkout -b vulcan
git log

vim salve.py 
```
```python
# --start
import sys

def default():
    print('o que voce quer?')

def vulcan():  #add
    print('dif-tor heh smusma')  #add

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'vulcan':  #add
            vulcan()  #add
        else:
            print (sys.argv[1])
    else:
        default()

if __name__ == '__main__':
    main()
# --end
```
```bash
git status 
git diff
git add salve.py 
git commit -m 'Vulcanos encontrados'
git log --all --graph --decorate --oneline
```

Ok. Agora temos três ramos de desenvolvimento distintos. Chegou o momento de unir os esforços de humanos, klingons e vulcanos em um único código utilizando o comando **git merge**:

```bash
git checkout master
git merge klingon
```

Aparentemente, a primeira união (merge) ocorreu sem problemas, e a função klingon() foi incorporada em master. 

```bash
git merge vulcan
git merge --abort
```

Entretanto, como o ramo vulcan partiu de um estado anterior ao atual, **git** está indicando um conflito na função **main()** ao tentar realizar a união. Vamos identificar e resolver esse conflito manualmente:

```bash
git merge vulcan
vim salve.py
```
```python
# --
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'klingon':  #add
            klingon()
        elif sys.argv[1] == 'vulcan':  #add
            vulcan()  #add
        else:
            print (sys.argv[1])
    else:
        default()
# --
```
```bash
git merge --continue
```

Agora o código salve.py tem ambas as funções (klingon e vulcan) implementadas.

Mais detalhes sobre `branches` e `merge` podem ser vistos, por exemplo, no [Pro Git Book](https://git-scm.com/book/pt-br/v2/Git-Branching-Basic-Branching-and-Merging).

## Git online

### Git clone e git pull (baixando repositórios existentes)

Muitas vezes, gostaríamos de fazer download do conteúdo de um repositório para ter os arquivos localmente.
Isso é comum até mesmo para programas cujo código fonte é armazenado no GitHub, e temos que baixar os arquivos para compilar.
A maneira mais fácil de fazer o download do conteúdo, é com o `git clone`, que baixa os arquivos do repositório, e também os metadados do **git**

```bash
git clone <url>
```

Esse comando fará o download do repositório criando um novo diretório no diretório atual, com o nome do repositório.

Dentro de um diretório clonado (ou que você adicionou um `remote`, conforme explicado abaixo) você pode atualizar para a última versão no servidor, do ramo que você está usando:

```bash
git pull
```

Que faz um *fetch* dos commits mais novos no repositório e realiza um merge automaticamente, te levando a última versão disponível naquele ramo.

### Git remote (colaborando com outras pessoas online)

Se você tem um repositório local (que não foi baixado com git clone) e quer colaborar com outras pessoas, está na hora de enviar seu repositório local para um servidor remoto utilizando **git remote**.

```bash
git remote add origin <url>
git push -u origin master
git log --all --graph --decorate --oneline
```

O comando `git remote add`, adicionam ao repositório a fonte remota `<url>`, por exemplo, o GitHub, chamando-a de `origin`.
Já o comando `git push` é utilizado para enviar as mudanças feitas localmente no seu computador para o servidor remoto, nesse caso, enviando ao servidor `origin` o ramo `master`.
Note que você pode enviar outros ramos, e manter uma cópia remota deles.
Finalmente, o `git log` é utilizado para mostrar o histórico de mudanças desse repositório, com as flags indicadas com `--` sendo opções de visualização.

A `<url>` para a qual você enviará o seu repositório pode ser a url de um repositório do GitHub.
Para isso, você precisa primeiro criar um repositório no GitHub para receber o seu projeto.
Isso pode ser feito clicando no sinal de `+` presente na barra superior (entre o sino de notificações e sua foto) quando está logado no GitHub.
Crie um repositório com o nome desejado e sem inicializá-lo com nenhum arquivo (sem README, .gitignore e licença).
Na página seguinte (a página inicial do repositório vazio), aparecerá um link como `git@github.com:hmcezar/teste.git`.
Essa é a url do repositório que será adicionada com o `git remote`.
Mais informações podem ser vistas na [documentação](https://docs.github.com/pt/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line) do próprio GitHub.

Alternativamente, se você ainda não tem um repositório para o projeto atual, é possível criar um repositório com o arquivo README pela interface do GitHub e depois clona-lo.
Depois de clonado, você pode adicionar os arquivos desejados e fazer um *commit* e *push* (como acima) para enviar os arquivos para o GitHub.
Note que este também é o procedimento que deve seguir para enviar *commits* para um repositório que você tenha permissão de escrita.
Para repositórios que você não tem permissão de escrita é necessário criar um [*pull request*](https://docs.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request), o que foge do escopo desse tutorial.

### Usando outras funcionalidades do GitHub
Além de servir como servidor para repositórios **git**, o GitHub possui outras funcionalidades.
Por exemplo, todo repositório **git** no GitHub conta com um **issue tracker**, que pode ser utilizado por usuários e desenvolvedores para acompanhar e reportar bugs e/ou requisitar novas funcionalidades.

O caráter colaborativo do GitHub também fica claro devido aos **pull requests**.
Os *pull requests* são sugestões de *commits* que outros usuários que não são necessariamente desenvolvedores naquele projeto podem fazer.
Além disso, é possível utilizar no GitHub ferramentas para teste automático, coordenar o projeto com painéis parecidos como no Trello, e uma variedadade de outras facilidades.
Essas funcionalidades fogem do escopo desse tutorial, contudo, são importantes espcialmente para projetos grandes e complexos.

### Comandos adicionais

Se você pretende utilizar **git** em seus projetos, procure por mais informações sobre os comandos:

- **git config** ou vim ~/.gitconfig
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

Mais informações podem ser encontradas nas referências:
- Pro Git Book: https://git-scm.com/book/pt-br/v2
- Documentação do GitHub: https://docs.github.com/pt
- Markdown cheat-sheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
