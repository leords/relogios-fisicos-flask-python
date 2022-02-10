from flask import Flask
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
import random

auth = HTTPBasicAuth()
app = Flask(__name__)

# Flask é um micro framework que utiliza a linguagem Python para criar aplicativos Web. 

##variavel que aloca os horarios.
tempoRecebido = []

# !
@app.route('/relogio', methods=['GET'])
def obter_relogio():
    return jsonify({'tempoRecebido': tempoRecebido})


## Pegando o <T2> (horario que saiu a msg) e adicionando na lista[tempoRecebido] e retornando a própria lista para o cliente!
## array qual já foi armazenada <T1>, <T2>, <T3>
@app.route('/enviar-relogio', methods=['GET'])
def att_relogio():
    
    # random para criar a defasagem!
    numberRambom = random.randrange(5, 10) 

    # Gerando o <t2>

    #pegando o datetime atual da maquina
    horarioAtual = datetime.now()
    hora = horarioAtual.hour 
    minuto = horarioAtual.minute 
    segundo = horarioAtual.second 

    #timedelta com o horario, minuto e segundos da maquina
    horaCerta = timedelta(hours=hora, minutes=minuto, seconds=segundo)
    #timedelta apenas com -5 segundos
    horaDefasagem = timedelta(seconds=numberRambom)

    #soma dos dois timeDelta e passando como strinf para 'horarioSomado'.
    horarioSomado = str(horaCerta+horaDefasagem)
    
    # Separando para pegar apenas os segundos da string, 
    # Puxando direto o 'horaDefasagem.total_seconds' retornava do tipo 'b' e não era possivel ler pelo parametros
    # e também não convertia com o valor correto!
    segundosDefasados = horarioSomado.split(':')
    print('spliit', segundosDefasados[2])
    
    params ={
        'nome': 'T2',
        'hora': hora,
        'minuto': minuto,
        'segundo': segundosDefasados[2]
    }

    tempoRecebido.append(params)

    #retornando a array 'tempoRecebido' para cliente com <T0> <T1> <T2>
    return jsonify({
        'tempoRecebido': tempoRecebido
        })


#POST recebendo <T0> do cliente e pegando o <T1> aqui do servidor, momento em que chegou <T0>! 
# Ambos sendo salvo na array 'tempoRecebido';
@app.route('/relogio', methods=['POST'])
def receber_hora():
    if not request.json or not 'nome' in request.json:
        abort(400)
    # Chegando o <t0> via post do cliente
    tempo = {
        'nome': request.json['nome'],
        'hora': request.json.get('hora', ""),
        'minuto': request.json.get('minuto', ""),
        'segundo': request.json.get('segundo', "")
    }

    # salvando na lista tempoRecebido!
    tempoRecebido.append(tempo)

    # Agora pegando o tempo <T1> //horario em que chegou o T0 
    horarioAtual = datetime.now()
    hora = horarioAtual.hour
    minuto = horarioAtual.minute
    segundo = horarioAtual.second

    tempoSistema = {
        'nome': 'T1',
        'hora': hora,
        'minuto': minuto,
        'segundo': segundo
    }

    tempoRecebido.append(tempoSistema)
    return jsonify({'tempo': tempo}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)

if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)