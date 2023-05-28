import socket
import time
from tkinter import *
from tkinter import ttk
from threading import *
import RSA
from RSA import *
import random
import re

is_new_msg = False
king_of_data = ""
my_name = ""
users_data = ""
is_username_ok = ""
users_list = []
# PORT = 32465
PORT = 7727
public_k = 0
private_k = 0
server_public_key = 0

# host = input("ip address (193.161.193.99): ")
host = input("ip address (127.0.0.1): ")
if host == "":
    host = "127.0.0.1"
my_socket = socket.socket()
my_socket.connect((host, PORT))

window = Tk()
window.title("NBS.CHAT")
w_lu = Toplevel()
w_lu.withdraw()

ent_the_msg = ttk.Entry(w_lu, width=30)
window.resizable(False, False)
window.geometry("400x400")

# Set the initial theme
window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "dark")


def prime_num():
    global public_k
    global private_k
    primes = [i for i in range(15, 1000) if RSA.is_prime(i)]
    n = random.choice(primes)
    n2 = random.choice(primes)
    if n2 == n:
        while n2 == n:
            n2 = random.choice(primes)

    public_k, private_k = RSA.keys(n, n2)


def disconnect():
    my_socket.send(f"0{my_name}".encode())
    w_lu.withdraw()


def refresh():
    global users_list, users_data, is_new_msg
    my_socket.send("2".encode())

    while True:

        if is_new_msg:
            break
        time.sleep(0.15)
    is_new_msg = False

    users_list.clear()
    users_list = users_data.strip("\n").split("\n")
    user_select.configure(values=users_list)
    user_select.current(0)


ll1 = ttk.Label(window, text="Join to NBS.CHAT", font=("Arial", 15))

l_un = ttk.Label(window, text="USER NAME -")

e_un = ttk.Entry(window, width=30)
user_select = ttk.Combobox(w_lu, values=users_list)

user_select.get()
# text

chat_nbs = Text(w_lu, width=112)


# all_users_list = ttk.Notebook(w_lu, width=400, height=280)


def insert_msg(k_of_data):
    chat_nbs.configure(state='normal')
    chat_nbs.insert(END, f"{k_of_data}\n")
    chat_nbs.configure(state='disabled')
    print("msg inserted!")


def get_msg():
    global king_of_data, is_username_ok, users_data, is_new_msg, server_public_key
    while True:
        king_of_data = my_socket.recv(4096).decode()

        if king_of_data[0] == "0":
            king_of_data = king_of_data[1:]

            is_username_ok = " ".join(king_of_data.split()[0])
            is_username_ok = re.sub(r'\s+', '', is_username_ok)

            key_of_user = " ".join(king_of_data.split()[1:])
            key_of_user = re.sub(r'\s+', '', key_of_user)
            res = eval(key_of_user)
            server_public_key = res
            is_new_msg = True

        elif king_of_data[0] == "1":
            users_data = king_of_data[1:]
            is_new_msg = True

        elif king_of_data[0] == "3":
            king_of_data = king_of_data[1:]
            king_of_data = king_of_data.replace("[", "")
            king_of_data = king_of_data.replace("]", "")

            um_list = list(king_of_data.split(","))

            try:
                um_list = list(map(int, um_list))

            except TypeError:
                um_list = [25, 15]

            king_of_data = decrypt(private_k, um_list)
            insert_msg(king_of_data)

        elif king_of_data[0] == "4":
            king_of_data = king_of_data[1:]
            king_of_data = king_of_data.replace("[", "")
            king_of_data = king_of_data.replace("]", "")

            um_list = list(king_of_data.split(", "))
            try:
                um_list = list(map(int, um_list))

            except TypeError:
                um_list = [25, 15]

            king_of_data = decrypt(private_k, um_list)
            insert_msg(king_of_data)

        else:
            print("something is wrong...")


def send(name, msg):
    msgs = f"{my_name} {name} {msg}"
    f_msg = RSA.encrypt(server_public_key, msgs)
    final_msg = f"3{f_msg}"
    ent_the_msg.delete(0, END)
    my_socket.send(final_msg.encode())


def clear():
    chat_nbs.configure(state='normal')
    chat_nbs.delete("1.0", "end")
    chat_nbs.configure(state='disabled')


def choose_user():
    global users_list
    global king_of_data
    window.withdraw()
    w_lu.deiconify()
    w_lu.geometry("800x550")
    w_lu.resizable(False, False)
    w_lu.title(my_name)
    refresh()

    # entry
    ent_the_msg.bind("<Return>",
                     lambda event: [send(user_select.get(), ent_the_msg.get()), ent_the_msg.insert(END, "")])
    # buttons
    btn_clear = ttk.Button(w_lu, text="clear the chat", command=lambda: clear())
    btn_refresh = ttk.Button(w_lu, text="refresh the users list", command=lambda: refresh())
    btn_ok = ttk.Button(w_lu, text="send",
                        command=lambda: [send(user_select.get(), ent_the_msg.get()), ent_the_msg.insert(END, "")])
    # temp solution to recv msgs:
    btn_disconnect = ttk.Button(w_lu, text="disconnect", command=lambda: disconnect())

    chat_nbs.grid(padx=5, pady=5, row=0, column=0, columnspan=5, sticky="nsew")
    btn_refresh.grid(pady=5, padx=5, row=1, column=0, sticky="nsew")
    user_select.grid(pady=5, padx=5, row=1, column=1, sticky="nsew")
    btn_clear.grid(pady=5, padx=5, row=1, column=2, sticky="nsew")

    ent_the_msg.grid(padx=5, pady=5, row=2, column=0, columnspan=4, sticky="nsew")
    btn_ok.grid(padx=5, pady=5, row=2, column=4, sticky="nsew")
    btn_disconnect.grid(padx=5, pady=5, row=3, column=3, columnspan=2, sticky="nsew")


def pending_approval():
    global my_name, is_username_ok, is_new_msg
    my_name = e_un.get()
    if my_name.count(" ") != 0:
        my_name = my_name.split()[0]

    final_msg = f"1{my_name} {public_k}"
    my_socket.send(final_msg.encode())

    while True:
        if is_new_msg:
            break
        time.sleep(0.25)
    is_new_msg = False
    if is_username_ok == "next":
        choose_user()

    else:
        e_un.delete(0, END)
        e_un.insert(0, "This username is not available")


def login():
    ll1.pack(padx=5, pady=5)

    l_un.pack(padx=5, pady=5)
    e_un.bind("<Return>", lambda event: pending_approval())
    e_un.pack(padx=5, pady=5)

    b_join = ttk.Button(window, text="LOGIN", command=lambda: pending_approval())
    b_join.pack(padx=5, pady=5)


def main():
    prime_num()
    login()
    # encryption_rsa()
    get_msg_thread = Thread(target=lambda: get_msg())
    get_msg_thread.start()
    window.mainloop()


if __name__ == "__main__":
    main()
