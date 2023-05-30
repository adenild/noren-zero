import datetime
from auth import create_user, login
from wallet import add_amount, check_wallet, history_on_period, remove_amount

user_data = []
while not user_data:
    acao = input("O que você gostaria de fazer? \n \
                1. Login \n \
                2. Cadastrar uma nova conta \n \
                0. fechar o programa \n \
                R: ")
    if acao == "1":
        user_data = login()
    elif acao == "2":
        user_data = create_user()
    elif acao == "0":
        break
    else:
        print("ação inválida")
        
if user_data:
    ui = ""
    while ui != "0":
        ui = input("o que gostaria de fazer? \n \
                1. ver seu saldo \n \
                2. ver extrato \n \
                3. adicionar saldo \n \
                4. remover saldo \n \
                0. sair \n \
                R: ")
        if ui == "1":
            check_wallet(user_data["wallet_id"],
                         user_data["user_id"])
        elif ui == "2":
            ui2 = input("você gostaria de ver o extrato de \n \
                1. um período específico \n \
                2. dos ultimos 10 dias \n \
                3. dos ultimos X dias \n \
                0. voltar ao menu anterior \n \
                R: ")
            if ui2 == "1":
                history_on_period(user_data["wallet_id"])
            elif ui2 == "2":
                today = datetime.datetime.now()
                ten_days = datetime.timedelta(10)
                history_on_period(user_data["wallet_id"], today-ten_days, today)
            elif ui2 == "3":
                today = datetime.datetime.now()
                x_days = datetime.timedelta(float(input("quantos dias de histórico você deseja ver? ")))
                history_on_period(user_data["wallet_id"], today-x_days, today)
        elif ui == "3":
            add_amount(user_data["wallet_id"],
                       float(input("quanto você gostaria de adicionar? ").replace(",", ".")))
        elif ui == "4":
            remove_amount(user_data["wallet_id"],
                          float(input("quanto você gostaria de remover? ").replace(",", ".")))
        elif ui == "0":
            break
        else:
            print("ação inválida")
        
