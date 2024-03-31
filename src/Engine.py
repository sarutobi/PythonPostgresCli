import datetime

from threading import Event, Thread
from time import sleep
#from sqlalchemy import create_engine

import settings
from Client import ConnectedClient

timedelta = 10
num_clients = 10

threads = []
stop_all = Event()

for i in range(0,num_clients) :
    client = ConnectedClient(settings.DB_URL, stop_all)
    thread = Thread(target=client.execute)
    threads.append(thread)
    thread.start()

curtime = datetime.datetime.now()
tilltime = curtime + datetime.timedelta(seconds=timedelta)

while (datetime.datetime.now() < tilltime):
    sleep(1)

# Устанавливаем флаг завершения клиентов
stop_all.set()

for t in threads:
    t.join()

#while(True):
#    for client in list_clients:
#        proc = Process(target=client.execute, args=("select current_time",))
#        procs.append(proc)
#        proc.start()
#        if datetime.datetime.now() < tilltime:
#            break

#    for proc in procs:
#        proc.join()

