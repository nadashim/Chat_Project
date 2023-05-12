import socket
import time
from tkinter import *
from tkinter import ttk
from threading import *
import RSA
from RSA import *
import random

# from tkinter import filedialog
# from RSA import *
# import random
# import os

is_new_msg = False
king_of_data = ""
my_name = ""
users_data = ""
users_list = []
PORT = 9999
is_username_ok = "not"
public_k = 0
private_k = 0

host = input("ip address (127.0.0.1): ")
if host == "":
    host = "127.0.0.1"
my_socket = socket.socket()
my_socket.connect((host, PORT))

window = Tk()
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
    primes = [i for i in range(15, 1000) if is_prime(i)]
    n = random.choice(primes)
    n2 = random.choice(primes)
    if n2 == n:
        while n2 == n:
            n2 = random.choice(primes)

    public_k, private_k = RSA.keys(n, n2)
    print(public_k, private_k)


def disconnect():
    my_socket.send("0".encode())
    w_lu.withdraw()


ll1 = ttk.Label(window, text="Join the chat", font=("Arial", 15))

l_un = ttk.Label(window, text="USER NAME -")

e_un = ttk.Entry(window, width=30)

user_select = ttk.Combobox(w_lu, values=users_list)
user_select.get()

# text
all_users_list = Text(w_lu, width=112)


# def receive():
#     while True:
#         data = my_socket.recv(1024).decode()
#         print(data)
#         all_users_list.insert(END, data + "\n")


def refresh():
    global users_list, users_data, is_new_msg
    my_socket.send("2".encode())

    while True:

        if is_new_msg:
            break
        time.sleep(0.25)
    is_new_msg = False

    print(f"users: {users_data}")
    users_list.clear()
    users_list = users_data.strip("\n").split("\n")
    print(users_list)
    user_select.configure(values=users_list)
    user_select.current(0)


def insert_msg(k_of_data):
    all_users_list.configure(state='normal')
    all_users_list.insert(END, f"{k_of_data}\n")
    all_users_list.configure(state='disabled')
    print("msg inserted!")


def get_msg():
    """
    for data type 3 (send to yourself):
    ...
    :return:
    """
    global king_of_data, is_username_ok, users_data, is_new_msg
    while True:
        king_of_data = my_socket.recv(1024).decode()
        print(f"king_of_data: {king_of_data}")

        if king_of_data[0] == "0":
            is_username_ok = king_of_data[1:]
            is_new_msg = True

        elif king_of_data[0] == "1":
            print(f"users list recv")
            users_data = king_of_data[1:]
            is_new_msg = True

        elif king_of_data[0] == "3":
            king_of_data = king_of_data[1:]
            insert_msg(king_of_data)

        elif king_of_data[0] == "4":
            king_of_data = king_of_data[1:]
            insert_msg(king_of_data)
            my_socket.send("5".encode())
            print(king_of_data)

        else:
            print("something is wrong...")


def send(name, msg):
    final_msg = f"3{my_name} {name} {msg}"
    ent_the_msg.delete(0, END)
    my_socket.send(final_msg.encode())
    print(f"final_msg: {final_msg}")

    # king_of_data = my_socket.recv(1024).decode()
    # print(king_of_data)
    # # insert_msg()


def choose_user():
    global users_list
    global king_of_data
    window.withdraw()
    w_lu.deiconify()
    w_lu.geometry("800x550")
    w_lu.resizable(False, False)
    w_lu.title(my_name)
    refresh()
    # data = my_socket.recv(1024).decode()

    # entry
    ent_the_msg.bind("<Return>",
                     lambda event: [send(user_select.get(), ent_the_msg.get()), ent_the_msg.insert(END, "")])
    # buttons
    btn_refresh = ttk.Button(w_lu, text="refresh the users list", command=lambda: refresh())
    btn_ok = ttk.Button(w_lu, text="send",
                        command=lambda: [send(user_select.get(), ent_the_msg.get()), ent_the_msg.insert(END, "")])
    # temp solution to recv msgs:
    btn_disconnect = Button(w_lu, text="disconnect", command=lambda: disconnect())

    all_users_list.grid(padx=5, pady=5, row=0, column=0, columnspan=5, sticky="nsew")
    btn_refresh.grid(pady=5, padx=5, row=1, column=0, sticky="nsew")
    user_select.grid(pady=5, padx=5, row=1, column=1, sticky="nsew")

    ent_the_msg.grid(padx=5, pady=5, row=2, column=0, columnspan=4, sticky="nsew")
    btn_ok.grid(padx=5, pady=5, row=2, column=4, sticky="nsew")
    btn_disconnect.grid(padx=5, pady=5, row=3, column=3, columnspan=2, sticky="nsew")

    #     king_of_data = my_socket.recv(1024).decode()
    #     if king_of_data[0] == "3":
    #         king_of_data = king_of_data[1:]
    #         insert_msg()
    # #


def pending_approval():
    global my_name, is_username_ok, is_new_msg
    my_name = e_un.get()
    if my_name.count(" ") != 0:
        my_name = my_name.split()[0]

    final_msg = "1" + my_name
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
