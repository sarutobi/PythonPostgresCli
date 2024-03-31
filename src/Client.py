
import signal
from time import sleep
from sqlalchemy import create_pool_from_url, text


class BaseClient:
    """ Base client """    

    def __init__(self, db_url:str, stop_now:bool) -> None:
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.db_pool = create_pool_from_url(db_url)
        self.stop_now = stop_now

    def stop(self, signum, frame):
        self.stop_now = True

    def execute(self) -> None:
        pass
class QueryClient(BaseClient):
    """ Client that perform only select queries"""
    def __init__(self, db_url: str, query:str) -> None:
        super().__init__(db_url)
        self.query = query

    def execute(self):
        while (not self.stop_now):
            with self.db_pool.connect() as conn:
                conn.execute(text(self.query))

            sleep(1)

class ConnectedClient(BaseClient):
    """This client hold open connection and do nothing"""

    def __init__(self, db_url:str, stop:bool) -> None:
        super().__init__(db_url, stop)

    def execute(self) -> None:
        conn = self.db_pool.connect()

        while (not self.stop_now.is_set()):
            sleep(1)
        