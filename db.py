import psycopg2
from dotenv import dotenv_values

env_vars = dotenv_values('.env')

def connect_db(arquivo_raw):
    # prod
    conn = psycopg2.connect(
        dbname="gplofpcr",
        user=env_vars['POSTGRES_USER'],
        password=env_vars['POSTGRES_PASS'],
        host="silly.db.elephantsql.com",
        port="5432"
    )
    """# dev
    conn = psycopg2.connect(
        dbname="noren-zero",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )"""
    arquivo_origem = "\\".join(arquivo_raw.split("\\")[-2:])
    print(f'{arquivo_origem} fez uma conexão no banco')
    return conn