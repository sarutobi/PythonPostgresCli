
from sqlalchemy import text


class BaseClient:
    """ Base client """    
    
    def __init__(self, engine) -> None:
        self.engine = engine

    def execute(self, query:str) -> None:
        with self.engine.connect() as conn:
            conn.execute(text(query))