import random
from datetime import datetime, timedelta
import requests
 
def main():

    numberRambom = random.randrange(5, 10) 

    # Pegando o datetime atual da maquina
    horarioAtual = datetime.now()
    hora = horarioAtual.hour 
    minuto = horarioAtual.minute 
    segundo = horarioAtual.second 

    # Setando na variavel Timedelta com o horario, minuto e segundos da maquina
    horaCerta = timedelta(hours=hora, minutes=minuto, seconds=segundo)
    # Setando na variavel Timedelta apenas com -5 segundos
    horaDefasagem = timedelta(seconds=-numberRambom)

    # **** TimeDelta permite calcular a diferenca entre dois horario!!!! *****

    #somando as duas datas (certa e com defasagem).
    horasSomadas = str(horaCerta+horaDefasagem)

    # Separando para pegar apenas os segundos da string, 
    # Puxando direto o 'horaDefasagem.total_seconds' retornava do tipo 'b' e não era possivel ler pelo parametros
    # e também não convertia com o valor correto!
    segundosDefasados = horasSomadas.split(':')

    # Criando o parametro a ser enviando pelo post "/relogio".
    
    params ={
        'nome': 'T0',
        'hora': hora,
        'minuto': minuto,
        'segundo': segundosDefasados[2]
    }

    # Enviando ao servidor o horario já com a defasagem! <T0>.
    requests.post('http://127.0.0.1:5000/relogio', json=params)


    # Fazendo essa requisição vamos receber os horarios <T0>, <T1>, <T2>
    r = requests.get("http://127.0.0.1:5000/enviar-relogio")

    data = r.json()

    print(data)
    for i in range(len(data['tempoRecebido'])):
        # condição procurando pelo nome dos tempos e alocando os valores nas variaveis
        if (data['tempoRecebido'][i]['nome'] == "T0"):
                horaT0 = data['tempoRecebido'][i]['hora']
                minutoT0 = data['tempoRecebido'][i]['minuto']
                segundoT0 = data['tempoRecebido'][i]['segundo']
                # setando os valores com o metodo timeDelta para realizar os calculos.
                T0 = timedelta(hours = int(horaT0), minutes = int(minutoT0), seconds = int(segundoT0), microseconds=0)

        elif (data['tempoRecebido'][i]['nome'] == "T1"):
                horaT1 = data['tempoRecebido'][i]['hora']
                minutoT1 = data['tempoRecebido'][i]['minuto']
                segundoT1 = data['tempoRecebido'][i]['segundo']

                T1 = timedelta(hours = int(horaT1), minutes = int(minutoT1), seconds = int(segundoT1), microseconds=0)

        elif (data['tempoRecebido'][i]['nome'] == "T2"):
                horaT2 = data['tempoRecebido'][i]['hora']
                minutoT2 = data['tempoRecebido'][i]['minuto']
                segundoT2 = data['tempoRecebido'][i]['segundo']
                
                T2 = timedelta(hours = int(horaT2), minutes = int(minutoT2), seconds = int(segundoT2), microseconds=0)

    M1 = T1 - T0
    print("HORA T0 =", T0)
    print("HORA T1 =", T1)
    print("Mensagem 1 =", M1)

    # Criando o <T3> que é igual o <T0> + 5 segundos.
    T3 = T0 + timedelta(seconds = 5)

    M2 = T2 - T3
    print("\nHORA T2 =", T2)
    print("HORA T3 =", T3)
    print("Mensagem 2 =", M2)

    defasagem = (M1 + M2)//2
    print("\nDefasagem:", defasagem)

    T4 = timedelta(hours = horarioAtual.hour, minutes = horarioAtual.minute, seconds = horarioAtual.second, microseconds=0)
    print("\nTempo Atual:", T4)

    T4 = T4 + defasagem
    print("\nTempo Atual Ajustado:", T4)

if __name__ == "__main__":
    main()