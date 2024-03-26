from multiprocessing import Process
from time import sleep
from sqlalchemy import create_engine

import settings
from Client import BaseClient

list_clients = []
procs = []

engine = create_engine(settings.DB_URL, pool_size=5,echo=True)
for i in range(1,80) :
    client = BaseClient(engine)
    list_clients.append(client)

for i in range(1, 3):
    for client in list_clients:
        proc = Process(target=client.execute, args=("select current_time",))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

