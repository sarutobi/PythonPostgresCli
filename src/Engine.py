from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('postgresql+psycopg://postgres:123456@127.0.0.1/thai', echo=True)
with engine.connect() as conn:
    result = conn.execute(text("select count(*) from book.bus"))
    print(result.all())
