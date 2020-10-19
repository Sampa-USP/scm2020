#!/usr/bin/env python

'''am1.py: Código 1 utilizado na aula de introdução ao AM'''

__author__     = 'Camilo A F Salvador'
__email__      = 'csalvador@usp.br'

# Importando bibliotecas
import pandas as pd
from sklearn.datasets import load_diabetes

# Essas bibliotecas são necessárias para fazer os gráficos
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
plt.style.use('tableau-colorblind10')
plt.rcParams.update({'font.size': 10, 'figure.figsize': (8,4.5)})

## Sec 1. Carregando o banco de dados

x = load_diabetes()
target = 'Y'

# Definindo um título para cada coluna/var
df = pd.DataFrame(x.data, columns=x.feature_names)

print ('\n-- Dados iniciais --\n')
df[target] = x.target    # define a var-alvo
X = df.drop(target, 1)   # X será a matriz de var (features)
y = df[target]           # y será a var-alvo
print(df.head())         # imprime as primeiras linhas do banco de dados 'df'

# Exportando o banco de dados "df" para *.csv - ocpional
df.to_csv(r'Diabetes.csv', index=None, header=True)

# Normalizando os dados (neste exemplo, não é necessário)
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler(feature_range=(0, 1))
# X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

# Imprimindo a matriz de var X (inicial)
print('\nHá {} variáveis descritivas:\n{}'.format(X.shape[1], X.columns.values))

# Uma descrição gráfica simplificada do DF
bins = np.arange(np.floor(y.min()), np.ceil(y.max()), 10)
print (bins)

plt.title('Valores da var-alvo')
plt.hist(y, bins=bins, density=1, alpha=1, label='y')
plt.xlim(xmin= 0, xmax = 350)
plt.locator_params(axis='x', nbins=10)
plt.xlabel('Distribuição de y')
plt.ylabel('Probabilidade')
plt.yticks([])
plt.show()


## Sec 2.1. Correlação de Pearson

print ('\n-- Seção 2.1 --\n')
cor = df.corr(method='pearson')    # obtém a matriz de correlação

# Verifica a correlação com a var-alvo 'MEDV'
cor_target = abs(cor[target])
cor_target = cor_target.sort_values()

# Plotando a matriz de correlação
plt.title('Matriz de correlação de Pearson')
sns.heatmap(cor, annot=True, cmap=plt.cm.coolwarm)    # cores divergentes
# sns.heatmap(cor, annot=True, cmap=plt.cm.cubehelix) # cores lineares
plt.show()    # plota a matriz 

# Seleciona vars (features) que possuem alta correlação (>0.4) com a var-alvo
relevant_features = cor_target[cor_target>0.4]
print ('As variáveis com maior PCC em relação a var-alvo são:')
print ('{}\n'.format(relevant_features))

# Algumas var descritivas são fortemente correlacionadas (indesejado)
print ('As variáveis com maior PCC em relação a BMI são:')
cor_BMI = abs(cor['bmi'])
cor_BMI = cor_BMI.sort_values()
print (cor_BMI[cor_BMI>0.4])

# Outro jeito de verificar as correlações (matriz textual)
print ('\nA correlação entre BMI e s5 (lamotrigina) é:')
print(df[["bmi","s5"]].corr())

## Sec 2.2. PCA

print ('\n-- Seção 2.2 --\n')

from sklearn.decomposition import PCA

# Nessa notação, os dados não serão convertidos para pandas DFs
diabetes = load_diabetes()
X1 = diabetes.data
y1 = diabetes.target

# Note que a função PCA não recebe os valores de y
pca = PCA(n_components=2) 
X_pca = pca.fit_transform(X1)

print('Componentes de PC1 e PC2: {}\n'.format(abs( pca.components_ )))
print('A variância associada à PC1 e PC2: {}'.format(pca.explained_variance_ratio_))

# Visualização do espaço PCA vs duas variáveis arbitrárias
fig, ax = plt.subplots(1,2)
ps0 = ax[0].scatter(X['bmi'], X['s4'], c=y, cmap=plt.cm.coolwarm)
ax[0].set_xlabel('bmi')
ax[0].set_ylabel('s4')
ax[0].set_title('Antes do PCA')

ps1 = ax[1].scatter(X_pca[:,0], X_pca[:,1], c=y1, cmap=plt.cm.coolwarm)
ax[1].set_xlabel('PC1')
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_ylabel('PC2')
ax[1].set_title('Depois do PCA')
# fig.colorbar(ps1, ax=axes[1], shrink=0.8)

plt.show()

## Sec 2.3. RFECV

print ('\n-- Seção 2.3 --\n')

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFECV

reg = LinearRegression()
rfecv = RFECV(estimator=reg, step=1, cv=5, scoring='neg_mean_squared_error')
# (scoring) alternativos para regressão: 'r2', 'max_error'
rfecv.fit(X, y)

print("Número ótimo de variáveis descritivas: %d" % rfecv.n_features_)

plt.figure()
plt.title('NMSE da regressão linear vs número de variáveis')
plt.xlabel("Número de variáveis descritivas")
plt.ylabel("Desempenho")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()

## Sec 3. Regressão linear

print ('\n-- Seção 3 --\n')
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

bestfeatures = SelectKBest(score_func=f_regression, k=5)
fit = bestfeatures.fit(X, y)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(X.columns)

# concatena os dois dataframes para facilitar a visualização
featureScores = pd.concat([dfcolumns, dfscores], axis=1)
featureScores.columns = ['Variável','Score'] # nome para as colunas
print('Seleção univariável:')
print(featureScores.nlargest(10,'Score'))    # 10 melhores parâmetros

# Plotando para melhor visualização

feature_scores = pd.Series(fit.scores_, index=X.columns)
feature_scores.nlargest(5).plot(kind='barh')
plt.title('Variáveis selecionadas via regressão univariável (SelectKBest)')
plt.show()

## Sec 4. Penalização
print ('\n-- Seção 3 --\n')
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV, Lasso
from sklearn import metrics

reg = LassoCV(cv=5)
reg.fit(X, y)
print('Melhor score utilizando LassoCV com cv=5: %f' % reg.score(X,y))
coef = pd.Series(reg.coef_, index = X.columns)

print ('\nCoeficientes LassoCV:\n')
print (coef)
print('A rotina Lasso eliminaria ' +  str(sum(coef == 0)) + ' variáveis')

imp_coef = coef.sort_values()
imp_coef.plot(kind = "barh")
plt.title('Score das variáveis via regressão LassoCV')
plt.show()

y_pred = reg.predict(X)
print('Erro (MAE) utilizando todas as variaveis %f' % metrics.mean_absolute_error(y, y_pred))

X = X[['bmi', 'bp', 's5', 's4', 's6', 's1']] # s2, s3, age and sex excluded
reg.fit(X, y)
y_pred = reg.predict(X)
print('Erro (MAE) utilizando 6/10 var. selecionadas  %f' % metrics.mean_absolute_error(y, y_pred))

## -- fim -- 