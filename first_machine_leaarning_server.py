# -*- coding: utf-8 -*-
import string
import cherrypy
import pandas as pd
import numpy as np

from sklearn.model_selection  import train_test_split
from sklearn.tree import DecisionTreeRegressor

class RiscoCredito(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def probabilidade_risco_de_credito(self, historico_do_credito=1,divida=1,renda_anual=1000,garantia=1):
        df1 = pd.read_csv("dados_limitecredito.csv")
        data_treino = np.array(df1[['historico_credito', 'divida', 'garantias', 'renda']])
        data_classif = np.array(df1['Risco'])
        X_treino, X_teste, Y_treino, Y_teste = train_test_split(data_treino, data_classif, test_size=0.30)
        modelo_tree = DecisionTreeRegressor()
        arvore_classificacao = modelo_tree.fit(X_treino, Y_treino)
        #Executa a classificação
        res = modelo_tree.predict([[int(renda_anual),int(historico_do_credito), int(divida), int(garantia)]])

        #Encontra o valor da confidência
#         probabilidade = modelo_tree.predict_proba([[int(renda_anual), int(historico_do_credito), int(divida), int(garantia)]])
        probabilidade = 0

        if res == 1:
            classificacao = "Baixo"
        elif res == 2:
            classificacao = "Moderado"
        else:
            classificacao = "Alto"
        
        risco_credito = "Alto"
        probabilidade = 0
        dados = {
            "renda":renda_anual,
            "risco_credito":classificacao,
            "probabilidade":probabilidade,
        }
        return dados


if __name__ == '__main__':
    cherrypy.quickstart(RiscoCredito())
