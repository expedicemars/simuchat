import socket  # Hlavní modul pro funkci serveru
from threading import Thread  # Více procesů zároveň
import tkinter  # GUI
from tkinter import messagebox


def recv():
    while True:
        try:
            data = client_socket.recv(1024).decode()  # Zkouší obdržet zprávu
            msg_list.configure(state='normal')
            msg_list.insert(tkinter.END, data + '\n')
            msg_list.configure(state='disabled')
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
        top.withdraw()
        messagebox.showerror('Python Error', 'Error: Spojení se serverem bylo ztraceno!')


def on_closing(event=None):
    my_msg.set("quit")
    send()


SERVER_HOST = input('IP:')
SERVER_PORT = int(input('Port:'))

# Kostra GUI
top = tkinter.Tk()
top.title('SimuComm22')
top.geometry("770x450")

messages_frame = tkinter.Frame(top, bg='orange')


#messages_frame['bg'] = 'black'
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)

# Listbox který obsahuje zprávy
msg_list = tkinter.Text(messages_frame, yscrollcommand=scrollbar.set, bg="#26242f", fg='white')
scrollbar.config(command=msg_list.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_frame.pack(fill=tkinter.BOTH, expand=True)
msg_list.pack(padx=7, pady=7, fill=tkinter.BOTH, expand=True)
msg_list.config(font=("Unispace", 10))

# Řádek na psaní a tlačítko odeslat
entry_field = tkinter.Entry(messages_frame, textvariable=my_msg, bg="#26242f", fg='white')
entry_field.bind("<Return>", send)
entry_field.pack(padx=7, ipady=2, ipadx=265, side=tkinter.LEFT)
entry_field.config(font=('Arial', 10))
send_button = tkinter.Button(messages_frame, text="Odeslat", command=send, bg="#26242f", fg='white')
send_button.pack(padx=7, side=tkinter.LEFT)

top.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == '__main__':
    # IP adresa serveru, zjistíte pomocí Win+R -> ipconfig -> IPv4 Address
    # 127.0.0.1 pro local server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pouze přejmenované na client pro lepší vyznání
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        receive_thread = Thread(target=recv)
        receive_thread.start()
        tkinter.mainloop()
    except ConnectionRefusedError:
        top.withdraw()
        messagebox.showerror('Python Error', 'Error: Server nebyl nalezen!')
