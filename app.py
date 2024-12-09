from json import dumps, loads #bibliotecas do banco de dados
from flask import Flask, jsonify, request #importação da api 
from marshmallow import Schema, fields, ValidationError #importação da biblioeca marshmallow que tem os schemas que mantem tabelas, os fileds que é pra lidar com os arquivos e a ultima que é a de validação dos dados.

#duas  variaveis que recebem uma lista vazia para armazenar os dados abaixo
alunos = []
relatorios = []

# classe  Alunoschema que passa o parametro Schema para o banco que contem os atributos do banco como variaveis que sao idade e disciplina
class AlunoSchema(Schema):
    idade = fields.Integer(required=True) #idade vai receber fields um arquivo do tipo inteiro com uma var required que recebe o tipo verdadeiro
    disciplina = fields.String(required=True) # disciplina vai receber fields um arquivo do tipo string com uma var required qu recebe o tipo verdadeiro

# classe  RelatorioSchema que passa o parametro Schema para o banco que contem os atributos do banco como variaveis que sao titulo,criaçao e aluno
class RelatorioSchema(Schema):
    titulo = fields.Str() #titulo vai receber fields um arquivo do tipo string
    criacao = fields.Date() #criação vai receber fields date um arquivo que vai conter uma data
    aluno = fields.Nested(AlunoSchema()) #aluno vai receber fields nested que é um aninhamento de dados que vai permitir que você crie uma estrutura de dados complexa organizando os objetos dentro de ALunoSchema 

# funçao que cadastra alunos que recebe um json do tipo string
def cadastrarAluno(json_str: str):
    aluno = loads(json_str) #variavel aluno que vai carregar os dados do parametro jon_str
    alunos.append(aluno) #adiciona aluno dentro de uma lista atraves do append
    return aluno #retorna os dados da var aluno

#funçao para cadastrar relatorio  que recebe um json do tipo string
def cadastrarRelatorio(json_str: str):
    relatorio = loads(json_str) #variavel relatorio que vai carregar os dados do parametro jon_str
    relatorios.append(relatorio) #adiciona relatorio  dentro de uma lista atraves do append
    return relatorio #retorna relatorio

#nome da aplicação flask
app = Flask(__name__)

#metodo post com endpoint aluno
@app.post('/aluno')
def aluno_post(): #função aluno_post que vai adicionar os dados dentro de um json atraves do metodo post

    request_data = request.json #var request_data que recebe uma requisição para o json

    schema = AlunoSchema() #var schema que faz a modularizaçao chamando a class ALunoSchema junto com o conteudo dele
    try: #aqui ele vai tentar fazer os comandos abaixo
        result = schema.load(request_data) #var result que recebe o schema e o carrega carregando a requisição post dos dados do json

        data_now_json_str = dumps(result) #outra var que vai usar o metodo dump para enviar os dados da requisição post para o terminal atraves da var result

        response_data = cadastrarAluno(data_now_json_str) #var da resposta dos dados que passa o metodo cadastrarAluno junto com um novo parametro

    except ValidationError as err:   #uma exceção de validação de error definida como a var err
        return jsonify(err.messages), 400  #retorna a mensagemd de error 400 atraves do metodo jsonify no terminal caso ocorra o erro

    return jsonify(response_data), 200 #retorna a var response_data com o seu conteudo

#metodo post com endpoint relatorio
@app.post('/relatorio')
def relatorio_post():  #função relatorio_post que vai adicionar os dados dentro de um json atraves do metodo post

    request_data = request.json #var request_data que recebe uma requisição para o json

    schema = RelatorioSchema()  #var schema que faz a modularizaçao chamando a class RelatorioSchema junto com o conteudo dele
    try: #aqui ele vai tentar fazer os comandos abaixo
        result = schema.load(request_data) #var result que recebe o schema e o carrega carregando a requisição post dos dados do json


        data_now_json_str = dumps(result) #outra var que vai usar o metodo dumps para enviar os dados da requisição post para o terminal atraves da var result

        response_data = cadastrarRelatorio(data_now_json_str) #var da resposta dos dados que passa o metodo cadastrarRelatorio junto com um novo parametro

    except ValidationError as err:  #uma exceção de validação de error definida como a var err
        return jsonify(err.messages), 400 #retorna a mensagemd de error 400 atraves do metodo jsonify no terminal caso ocorra o erro

    return jsonify(response_data), 200 #retorna a var response_data com o seu conteudo

