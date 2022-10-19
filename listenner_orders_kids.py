import os
import time
import stomp

# Esse trexo de código é responsável por pegar as variáveis de ambiente responsáveis pela conexão com ActiveMQ
# Caso não encontre setará os dados a seguir como padrão
user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161

# Classe para ler as mensagens de Dias das Crianças
class ListennerOrdersKids(object):
    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, message):
        print(message.body)
        
# Conecta com ActiveMQ
conn = stomp.Connection()
lst = ListennerOrdersKids()

# Mostrar a Classe que irá escutar para ver se tem mensagem e executar a ação. 
conn.set_listener('', lst)
conn.connect(user, password, wait=True)

# Ler os topics para pegar os as mensagens filtradas do dias das crianças 
conn.subscribe(destination='/topic/pedidos', id=1, ack='auto', headers={'selector':"key = 'C'"})

while True:
    time.sleep(10)
