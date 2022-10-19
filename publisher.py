# Importando bibliotecas necessárias para a realização da atividade
import random
import sys
import os
import stomp

# Esse trexo de código é responsável por pegar as variáveis de ambiente responsáveis pela conexão com ActiveMQ
# Caso não encontre setará os dados a seguir como padrão
user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161


# Nessa variável é definido a quantidade de mensagens que deseja enviar, caso deseje gerar uma quantidade de mensagens maior é necessário apenas aumentar esse número 
messages = 50

# Aqui é onde é feito a conexão com activeMQ utilizando a lib stomp
conn = stomp.Connection()
conn.connect(user, password, wait=True)

# Trexo conténdo o dicionário com os tipos de mensagens que serão criadas para que possa ser gerado as mensagens randomicamente
erros_dict = {
    1: 'WARN',
    2: 'DEBUG',
    3: 'ERR',
    4: 'PROMOCAO'
}

promocoes_dict = {
    1: 'BlackFriday',
    2: 'DiaDosPais',
    3: 'DiaDasMaes',
    4: 'DiaDasCriancas'
}

# Laço de repitição no qual irá gerar a quantidade de mengasens configuradas, e randomicamente
for i in range(0, messages):
    # Gera um número de um a qatro aleatório para enviar mensagem randomica
    numero_aleatorio = random.randint(1, 4)
    
    # Toma a decisão de qual mensagem será enviada, se será uma fila um tópico ou fila. E colocar uma prioridade 
    if erros_dict[numero_aleatorio] == 'WARN':
        conn.send(body="WARN", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 1})
    elif erros_dict[numero_aleatorio] == 'DEBUG':
        conn.send(body="DEBUG", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 4})
    elif erros_dict[numero_aleatorio] == 'ERR':
        conn.send(body="ERR", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 9})
    else:
        headers = {}
        
        numero_aleatorio = random.randint(1, 4)
        pedido = promocoes_dict[numero_aleatorio]
        data = f"Promoção: {pedido} Id: {str(id)} "
        
        key=""
        if numero_aleatorio == 4:
            key="C"
            
        conn.send(body=data, destination="/topic/pedidos", persistent='false', key=key)

# Desconectar do ActiveMQ
conn.disconnect()