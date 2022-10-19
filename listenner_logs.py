import sys
import os
import time
import stomp

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "admin"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 8161

class ListennerOrders(object):
    def __init__(self):
        self.msg_list = []

    def on_error(self, headers, message):
        self.msg_list.append('(ERROR) ' + message)

    def on_message(self, message):
        print(message.body)
        
        
conn = stomp.Connection()
lst = ListennerOrders()
conn.set_listener('', lst)
conn.connect(user, password, wait=True)

# , headers={'order':"'priority': 1"}
conn.subscribe(destination='/queue/logs', id=1, ack='auto', headers={'sort':"'priority': 1"})

while True:
    time.sleep(10)

# conn.disconnect()
