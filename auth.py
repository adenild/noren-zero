import getpass

from psycopg2 import IntegrityError
from db import connect_db
from wallet import create_wallet

def create_user():
    username, password = input("usuário: "), getpass.getpass("senha: ")
    
    conn = connect_db(__file__)
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO auth.users (username, password) VALUES (%s, %s)", (username, password,)
        )
        conn.commit()
        print(f'usuário "{username}" criado com sucesso')
        cur.execute(
            "SELECT * FROM auth.users WHERE username = %s", (username,)
        )
        user = cur.fetchone()
        wallet_id = create_wallet(user[0])
        cur.close()
        conn.close()
        
        return {"user_id": user[0],"username": user[1],"wallet_id": wallet_id}

    except IntegrityError as e:
        print("usuário já existe")
        conn.rollback()
        cur.close()
        conn.close()
        return {}
    
    
def login():
    username = input("nome de usuário: ")
    conn = connect_db(__file__)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM auth.users WHERE username = %s", (username,)
    )
    user = cur.fetchone()  
    cur.close()
    conn.close()
    if user:
        password = getpass.getpass("senha: ")
        if password != user[2]:
            print("senha incorreta")
            return {}
        else:
            conn = connect_db(__file__)
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM wallet.wallets WHERE user_id = %s", (user[0],)
            )
            wallet = cur.fetchone()
            cur.close()
            conn.close()
            print("login realizado com sucesso")
            return {"user_id": user[0],"username": user[1],"wallet_id": wallet[0]}
    else:
        print("usuário não encontrado")
        return {}
    