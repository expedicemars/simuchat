import socket  # Hlavní modul pro funkci serveru
from threading import Thread  # Více procesů zároveň
import tkinter  # GUI
from tkinter import messagebox


def recv():
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Zkouší obdržet zprávu
            msg_list.insert(tkinter.END, data)
        except OSError:
            break


def send(event=None):
    try:
        message = my_msg.get()  # Napiš zprávu
        my_msg.set('')
        client_socket.send(bytes(message, 'utf8'))  # Odesílá zprávu serveru
        if message == 'quit':
            client_socket.close()
            top.quit()
    except ConnectionResetError:
        messagebox.showerror('Python Error', 'Error: Spojení se serverem bylo ztraceno!')


def on_closing(event=None):
    my_msg.set("quit")
    send()


# Kostra GUI
top = tkinter.Tk()
top.title('Komunikace simulace 2022 by Oto')
top.geometry("770x450")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Listbox který obsahuje zprávy
msg_list = tkinter.Listbox(messages_frame, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_frame.pack(fill=tkinter.BOTH, expand=True)
msg_list.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)
msg_list.config(font=("Unispace", 11))

# Řádek na psaní a tlačítko odeslat
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(padx=10, fill=tkinter.X)
send_button = tkinter.Button(top, text="Odeslat", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == '__main__':
    # IP adresa serveru, zjistíte pomocí Win+R -> ipconfig -> IPv4 Address
    # 127.0.0.1 pro local server
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5003
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pouze přejmenované na client pro lepší vyznání
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        receive_thread = Thread(target=recv)
        receive_thread.start()
        tkinter.mainloop()
    except ConnectionRefusedError:
        messagebox.showerror('Python Error', 'Error: Server nebyl nalezen!')
