from time import sleep
from sqlalchemy import create_engine
from sqlalchemy import text
import settings

list_conn = []

engine = create_engine(settings.DB_URL, pool_size=90,echo=True)
for i in range(1,80) :
    conn = engine.connect()
    list_conn.append(conn)
for i in range(1, 3):
    for conn in list_conn:
#with engine.connect() as conn:
        conn.execute(text("select current_time"))
        sleep(1)
    #print(result.all())
