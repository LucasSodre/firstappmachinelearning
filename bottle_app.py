#Autor: Lucas Camargo Sodre - 2018 -> projeto de bottle
#Conjunto de importacoes
from bottle import default_app, template, request, post, get
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeRegressor

#Definição das possíveis rotas para a função de callback

@get('/')
@get('/form/')
def index():
     #Definição de valores iniciais para as expressões animal, classificação e probabilidade
     return template('/firstappmachinelearning/formulariolimitecredito.html', animal = "-", classificacao = "-", probabilidade = "-")

#Definição da rota e função de callback
@post('/form/')
def index_resposta():
    #Pega os valores informados no formulário e atribui a variaveis locais
    renda_anual = request.forms.get('renda_anual')
    historico_do_credito = request.forms.get('historico_do_credito')
    divida = request.forms.get('divida')
    garantia = request.forms.get('garantia')

    modelo_tree = DecisionTreeRegressor()
    #Carrega o modelo gerado
    modelo_tree = joblib.load('/firstappmachinelearning/risco_de_credito_lucas_sodre_pos1.pkl')
    #Executa a classificação
    res = modelo_tree.predict([[int(renda_anual),int(historico_do_credito), int(divida), int(garantia)]])

    #Encontra o valor da confidência
    probabilidade = modelo_tree.predict_proba([[int(renda_anual), int(historico_do_credito), int(divida), int(garantia)]])

    if res == 1:
        classificacao = "Baixo"
    elif res == 2:
        classificacao = "Moderado"
    else:
        classificacao = "Alto"

    #Renderiza o template com os valores passados como argumento
    return template('/firstappmachinelearning/formulariolimitecredito.html', renda_anual = renda_anual, risco_credito = classificacao, probabilidade = probabilidade)

application = default_app()
