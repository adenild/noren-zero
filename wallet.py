import datetime
from db import connect_db
from rich.console import Console
from rich.table import Table


def create_wallet(user_id):
    conn = connect_db(__file__)
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO wallet.wallets (amount, user_id) VALUES (%s, %s)", (0, user_id)
    )
    conn.commit()
    
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE user_id = %s", (user_id,)
    )
    wallet = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return wallet[0]


def check_wallet(wallet_id, user_id):
    conn = connect_db(__file__)
    cur = conn.cursor()
    
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE id = %s AND user_id = %s", (wallet_id, user_id,)
    )
    wallet = cur.fetchone()
    
    cur.close()
    conn.close()
    print(f'o valor na carteira é de R${wallet[1]:.2f}')
    return(wallet[1])
    

def add_amount(wallet_id, amount):
    op_type = "+"
    conn = connect_db(__file__)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE id = %s", (wallet_id,)
    )
    wallet = cur.fetchone()
    wallet_amount = float(wallet[1])
    new_wallet_amount = wallet_amount + amount
    print(f'adicionando o montante de R${amount:.2f} na carteira')
    cur.execute(
        "UPDATE wallet.wallets SET amount=%s WHERE id = %s", (new_wallet_amount, wallet_id,)
    )
    cur.execute(
        "INSERT INTO wallet.operations(type, value, wallet_id) VALUES (%s, %s, %s)",
        (op_type, amount, wallet_id,)
    )
    conn.commit()
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE id = %s", (wallet_id,)
    )
    updated_wallet = cur.fetchone()
    cur.close()
    conn.close()
    print(f'o novo valor na carteira é de R${updated_wallet[1]:.2f}')
    return updated_wallet[1]


def remove_amount(wallet_id, amount):
    op_type = "-"
    conn = connect_db(__file__)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE id = %s", (wallet_id,)
    )
    wallet = cur.fetchone()
    wallet_amount = float(wallet[1])
    new_wallet_amount = wallet_amount - amount
    print(f'removendo o montante de R${amount:.2f} da carteira')
    cur.execute(
        "UPDATE wallet.wallets SET amount=%s WHERE id = %s", (new_wallet_amount, wallet_id,)
    )
    cur.execute(
        "INSERT INTO wallet.operations(type, value, wallet_id) VALUES (%s, %s, %s)",
        (op_type, amount, wallet_id,)
    )
    conn.commit()
    cur.execute(
        "SELECT * FROM wallet.wallets WHERE id = %s", (wallet_id,)
    )
    updated_wallet = cur.fetchone()
    cur.close()
    conn.close()
    print(f'o novo valor na carteira é de R${updated_wallet[1]:.2f}')
    return updated_wallet[1]


def history_on_period(wallet_id, data_menor=None, data_maior=None):
    if not data_maior or not data_menor:
        print(f"Dica: A data maior é a mais próxima do dia de hoje. Por exemplo: se hoje é dia {datetime.date.today()}, a maior data é a de hoje, e assim diminui.")
    if not data_menor:
        data_menor_raw = input("digite a data menor no formato [DD/MM/AAAA]: ")
        data_menor = datetime.datetime(int(data_menor_raw.split('/')[2]), int(data_menor_raw.split('/')[1]), int(data_menor_raw.split('/')[0]), 23, 59, 59)
    
    if not data_maior:
        data_maior_raw = input("digite a data maior no formato [DD/MM/AAAA]: ")
        data_maior = datetime.datetime(int(data_maior_raw.split('/')[2]), int(data_maior_raw.split('/')[1]), int(data_maior_raw.split('/')[0]), 23, 59, 59)
    
    conn = connect_db(__file__)
    cur = conn.cursor()

    # Execute a consulta SQL com as datas fornecidas
    cur.execute("SELECT * FROM wallet.operations WHERE wallet_id = %s AND created_at BETWEEN %s AND %s", (wallet_id, data_menor, data_maior))

    # Obtenha os resultados da consulta
    operacoes = cur.fetchall()
    # Feche o cursor e a conexão
    cur.close()
    conn.close()

    console = Console()
    table = Table(title="Operações", show_header=True)
    table.add_column("Tipo")
    table.add_column("Valor", justify="right")
    table.add_column("Data", justify="right")
    
    operacoes.reverse()
    
    for op in operacoes:
        table.add_row("Depósito" if op[1] == "+" else "Saque", f"R${op[2]:.2f}", f"{op[4].strftime('%d/%m/%Y %H:%M:%S')}", style="green" if op[1] == "+" else "red")

    console.print(table)

    return operacoes
