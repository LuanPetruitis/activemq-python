import sys
import os
import time
import stomp

# Esse trexo de código é responsável por pegar as variáveis de ambiente responsáveis pela conexão com ActiveMQ
# Caso não encontre setará os dados a seguir como padrão
user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161

# Classe para ler as mensagens 
class ListennerLogs(object):
    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, message):
        print(message.body)
        

# Conecta com ActiveMQ
conn = stomp.Connection()
lst = ListennerLogs()

# Mostrar a Classe que irá escutar para ver se tem mensagem e executar a ação. 
conn.set_listener('', lst)
conn.connect(user, password, wait=True)

# Ler fila para pegar os logs ordenados pela prioridade 
conn.subscribe(destination='/queue/logs', id=1, ack='auto', headers={'sort':"'priority': 1"})

# Loop infinito para manter conectado e pronto para ouvir mensagens
while True:
    time.sleep(10)
