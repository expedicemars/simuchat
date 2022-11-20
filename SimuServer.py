import socket  # Hlavní modul pro funkci serveru
from threading import Thread  # Více procesů zároveň
from datetime import datetime


def accept_connection():
    while True:
        print(f'[*] Čekám na připojení na adrese {SERVER_HOST}:{SERVER_PORT}')
        client, client_address = server_socket.accept()  # Přijme nové připojení
        print(f'[*]{client_address} se připojil.')
        client.send(bytes('Spojení se serverem bylo navázáno, pro vypnutí napiš quit, nyní vlož své jméno:', 'utf8'))
        addresses[client] = client_address
        Thread(target=log_client, args=(client,)).start()


def log_client(client):

    try:
        name = client.recv(1024).decode('utf8')
        welcome = f'Vítej {name}'
        client.send(bytes(welcome, 'utf8'))
        msg = f'{name} se připojil.'
        broadcast(bytes(msg, 'utf8'))
        clients[client] = name

    except ConnectionResetError:
        print(f'Klient se nepodařilo připojit.')
        client.close()

    while True:
        msg = client.recv(1024)
        date_now = datetime.now().strftime('%d-%m-%Y | %H:%M:%S')
        datename = f"[{date_now}] {name}"  # Formátování zprávy
        with open('chatlog.txt', 'a', encoding='utf-8') as log:  # Otevře log soubor
            log.write(datename + ': ' + msg.decode('utf8') + '\n')  # Zapisuje zprávu do logu
            log.close()
        if msg != bytes("quit", "utf8"):
            broadcast(msg, datename+": ")  # Posílá zprávu
        else:
            #client.send(bytes("quit", "utf8"))
            client.close()
            print(f'[*]{addresses[client]} se odpojil.')
            del clients[client]
            broadcast(bytes(f'{name} se odpojil.', encoding='utf8'))
            break


def broadcast(msg, prefix=""):  # Pošle zprávu všem klientům
    try:
        for sock in clients:
            sock.send(bytes(prefix, "utf8")+msg)

    except ConnectionResetError:
        print(f'Klient se násilně odpojil.')


if __name__ == '__main__':
    clients = {}
    addresses = {}
    clientslist = []
    # IP adresa serveru
    SERVER_HOST = socket.gethostbyname(socket.gethostname())
    SERVER_PORT = int(input('Port:'))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pouze přejmenované na server pro lepší vyznání
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Spojí host adresu a port dohromady
    server_socket.listen(10)  # Poslouchá pro 'x' zařízení

    ACCEPT_THREAD = Thread(target=accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

    server_socket.close()
