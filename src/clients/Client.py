from time import sleep
from sqlalchemy import NullPool, create_engine, text


class BaseClient:
    """ Base client """    

    def __init__(self, db_url:str, stop_now:bool) -> None:
        self.engine = create_engine(db_url, poolclass=NullPool)
        self.stop_now = stop_now

    def stop(self, signum, frame):
        self.stop_now.set()

    def execute(self) -> None:
        pass
class QueryClient(BaseClient):
    """ Client that perform only select queries"""
    def __init__(self, db_url: str, query:str) -> None:
        super().__init__(db_url)
        self.query = query

    def execute(self):
        while (not self.stop_now):
            with self.engine.connect() as conn:
                conn.execute(text(self.query))

            sleep(1)

class IdleClient(BaseClient):
    """This client hold open connection and do nothing - connection in idle state"""

    def __init__(self, db_url:str, stop:bool) -> None:
        super().__init__(db_url, stop)

    def execute(self) -> None:
        conn = self.engine.connect()

        while (not self.stop_now.is_set()):
            sleep(1)
        conn.close()

class IdleInTransactionClient(BaseClient):
    """This client hold open connection in open transaction state and do nothing - idle in transaction"""

    def __init__(self, db_url:str, stop:bool) -> None:
        super().__init__(db_url, stop)

    def execute(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text("begin transaction;"))
            while (not self.stop_now.is_set()):
                sleep(1)
            conn.rollback()
        # conn.close()

def client_factory(client_type: str, db_url:str, stop:bool) -> BaseClient:
    """ This is Factory for clients by type"""
    clients = {
        "Idle" : IdleClient,
        "IdleInTransaction": IdleInTransactionClient
    }
 
    if client_type not in clients.keys():
        raise ValueError("Unknown client type '{}'".format(client_type))
    
    return clients[client_type](db_url, stop)