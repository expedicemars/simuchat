import socket  # Hlavní modul pro funkci serveru
import time
from threading import Thread  # Více procesů zároveň
from datetime import datetime  # Pro zaznamenání času odeslání zprávy


def recv(conn, address):
    print("Připojil se: " + str(address))
    while True:
        try:
            data = conn.recv(1024).decode()  # Zkouší obdržet zprávu

            log = open('chatlog.txt', 'a', encoding='utf-8')  # Otevře log soubor
            log.write(str(data) + '\n')  # Zapisuje zprávu do logu
            log.close()

            print(str(data))  # Vypíše zprávu
        except ConnectionError:
            print(f"Spojení s klientem {address} bylo ztraceno.")  # Pokud klient spadne, server může zůstat zapnutý
            # a čeká znovupřipojení
            time.sleep(1)
            print(f"Čekám na opětovné připojení...")
            break


def send(conn, address):
    while True:
        try:
            message = input()  # Pošli zprávu
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Zaznamenání času odeslání zprávy
            message = f"[{date_now}] {name}: {message}"  # Formátování zprávy

            log = open('chatlog.txt', 'a', encoding='utf-8')  # Otevře log soubor
            log.write(str(message) + '\n')  # Zapisuje zprávu do logu
            log.close()
            conn.send(message.encode())  # Odesílá zprávu klientovi

        except ConnectionError:
            print('Zpráva nebyla odeslána, klient nenalezen...')
            break


def server_program():
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Spojí host adresu a port dohromady
    server_socket.listen(2)  # Poslouchá pro 'x' zařízení

    print(f"[*] Čekám na připojení {SERVER_HOST}:{SERVER_PORT}")
    while True:
        try:
            conn, address = server_socket.accept()  # Přijme nové připojení
            print ('prijmuto pripojeni')
            receiveThread = Thread(target=recv, args=(conn, address))  # Zapne thready s odesíláním a přijímáním zpráv
            sendThread = Thread(target=send, args=(conn, address))
            receiveThread.start()
            sendThread.start()
        except ConnectionError:
            break


if __name__ == '__main__':
    # IP adresa serveru
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5002
    name = 'MCC'  # Jméno zobrazené u zprávy (Mission Control Center)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pouze přejmenované na server pro lepší vyznání
    log = open('chatlog.txt', 'a', encoding='utf-8')
    server_program()  # Spustí celý program
