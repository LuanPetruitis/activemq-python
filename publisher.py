import random
import sys
import os
import stomp

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161

destination = sys.argv[1:2] or ["/topic/event"]
destination = destination[0]

messages = 100


conn = stomp.Connection()
conn.connect(user, password, wait=True)
# conn.start()
# conn.connect(login=user,passcode=password)

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

for i in range(0, messages):

    numero_aleatorio = random.randint(1, 4)
    if erros_dict[numero_aleatorio] == 'WARN':
        conn.send(body="WARN", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 1})
    elif erros_dict[numero_aleatorio] == 'DEBUG':
        conn.send(body="DEBUG", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 4})
    elif erros_dict[numero_aleatorio] == 'ERR':
        conn.send(body="ERR", destination="/queue/logs?jms.messagePrioritySupported=true", persistent='false', headers={"priority": 9})
    else:
        headers = {}
        
        numero_aleatorio = random.randint(1, 4)
        # numero_aleatorio = 4
        pedido = promocoes_dict[numero_aleatorio]
        data = f"Promoção: {pedido} Id: {str(id)} "
        
        key=""
        if numero_aleatorio == 4:
            key="C"
            # headers={"type":"Criança"}
        #     conn.send(body=data, destination="/topic/pedidos", headers=headers)
                
        conn.send(body=data, destination="/topic/pedidos", persistent='false', key=key)
        
    # erros = []
    # promocoes = []
    # data = "<pedido><id>"  + str(i) + "</id></pedido>"
    # conn.send(body=data, destination="/queue/promocoes", )
    
conn.disconnect()