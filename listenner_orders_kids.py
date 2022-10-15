from email.quoprimime import body_check
import sys
import os
import time
import stomp

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161

class ListennerOrdersKids(object):
    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, message):
        print(message.body)
        
        
conn = stomp.Connection()
lst = ListennerOrdersKids()
conn.set_listener('', lst)
conn.connect(user, password, wait=True)

conn.subscribe(destination='/queue/pedidos', id=1, ack='auto', headers={'selector':"key = 'C'"})
time.sleep(10)

while True:
    time.sleep(10)

# conn.disconnect()
