import argparse
import datetime
import signal
import sys
from threading import Thread, Event
from time import sleep

from  settings import DB_URL
from clients.Client import client_factory

def spawn_clients(client_type:str, num_clients:int, timedelta:int, ignore_time:bool):
    """ Spawn and start clients """
    threads = []

    for i in range(0,num_clients) :
        client = client_factory(client_type, DB_URL, stop_all)
        thread = Thread(target=client.execute)
        threads.append(thread)
        thread.start()

    curtime = datetime.datetime.now()
    tilltime = curtime + datetime.timedelta(seconds=timedelta)

    while (ignore_time or datetime.datetime.now() < tilltime):
        sleep(1)

    # Устанавливаем флаг завершения клиентов
    stop_all.set()

    for t in threads:
        t.join()

def interruption(signum, frame):
    stop_all.set()
    sys.exit(0)

if (__name__ == '__main__'):
    stop_all = Event()
    signal.signal(signal.SIGINT, interruption)
    signal.signal(signal.SIGTERM, interruption)

    parser = argparse.ArgumentParser(description="Test postgresql client")
    parser.add_argument("--clients", "-c", type=int, default=10, help='number of clients to spawn')
    parser.add_argument("--type", "-T", choices=['Idle', 'IdleInTransaction', 'SelectOne'], default='Idle', help='Type of spawned clients')
    timeset = parser.add_mutually_exclusive_group()
    timeset.add_argument("--time", "-t", type=int, default=60,  help='time to work in seconds')
    timeset.add_argument("--infinite", "-I", action='store_true', help='Run clients until break')
    

    args = (parser.parse_args())
    
    spawn_clients(client_type=args.type, num_clients=args.clients, timedelta=args.time, ignore_time=args.infinite)
