import socket  # Hlavní modul pro funkci serveru
import sys
import time
from threading import Thread  # Více procesů zároveň
from datetime import datetime  # Pro zaznamenání času odeslání zprávy


def recv():
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Zkouší obdržet zprávu
            if not data:
                sys.exit(0)
            print(str(data))
        except ConnectionResetError:
            print('Spojení se serverem bylo ztraceno')
            time.sleep(1)
            print(f"Čekám na opětovné připojení...")
            client_socket.close()
            break


def send():
    while True:
        try:
            message = input()  # Napiš zprávu
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"[{date_now}] {name}: {message}"  # Formátování zprávy
            client_socket.send(message.encode())  # Odesílá zprávu klientovi

        except ConnectionError:
            print('Zpráva nebyla odeslána, server nenalezen...')
            break


def client_program():
    while True:
        try:
            print(f"[*] Připojuji se k {SERVER_HOST}:{SERVER_PORT}...")
            client_socket.connect((SERVER_HOST, SERVER_PORT))  # Připojení k serveru
            print("[*] Připojeno.")

            Thread(target=send).start()  # Zapne thready s odesíláním a přijímáním zpráv
            Thread(target=recv).start()

        except ConnectionError:
            print("K zadané IP adrese se nelze připojit.")
            time.sleep(1)
            print("Zkouším znovu za 5 sekund...")
            time.sleep(5)
            break

if __name__ == '__main__':
    # IP adresa serveru, zjistíte pomocí Win+R -> ipconfig -> IPv4 Address
    # 127.0.0.1 pro local server
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5002
    name = 'Posádka'  # Jméno zobrazené u zprávy
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pouze přejmenované na client pro lepší vyznání
    client_program()  # Spustí celý program
