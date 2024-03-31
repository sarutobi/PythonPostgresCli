from dotenv import dotenv_values

# Database connection parameters
env = dotenv_values()
DB_URL='postgresql+psycopg://{}:{}@{}/{}'.format(env['POSTGRES_USER'], env['POSTGRES_PASSWORD'], env['POSTGRES_HOST'], env['POSTGRES_DB'])
