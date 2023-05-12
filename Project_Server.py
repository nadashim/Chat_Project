import socket
from threading import *
import RSA
from RSA import *
import random
import re

# import select
# from tkinter import *
# from math import *

public_k = 0
private_k = 0
PORT = 9999
clients_sockets_list = []
clients_threads = []
users_name = []


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


def new_client(server_socket):
    counter = 0
    while True:
        clients_sockets_list.append(None)
        clients_sockets_list[counter], client_address = server_socket.accept()
        print("Client connected")
        clients_threads.append(None)
        clients_threads[counter] = Thread(target=lambda: handle_client_msg(clients_sockets_list[counter]))
        clients_threads[counter].start()
        counter += 1


def handle_client_msg(client_socket):
    while True:
        print(clients_threads)
        print(clients_sockets_list)
        user_msg = client_socket.recv(1024).decode()
        check = True
        if user_msg[0] == "1":
            user_msg = user_msg[1:]

            if user_msg in users_name:
                check = False
            elif user_msg == "":
                check = False
            else:
                users_name.append(user_msg)
                print(users_name)

            if check:
                reply = "0next"
                client_socket.send(reply.encode())
            else:
                reply = "0false"
                client_socket.send(reply.encode())

        elif user_msg[0] == "2":
            f1 = ""
            for i in users_name:
                f1 += str(i) + "\n"
            client_socket.send(("1" + f1).encode())

        elif user_msg[0] == "3":
            user_msg = user_msg[1:]

            from_name = " ".join(user_msg.split()[0])
            from_someone = re.sub(r'\s+', '', from_name)

            to_name = " ".join(user_msg.split()[1])
            to_someone = re.sub(r'\s+', '', to_name)
            print(to_someone)
            msg = " ".join(user_msg.split()[2:])
            the_msg = msg

            final_msg = f"3{from_someone}: {the_msg}"
            number = users_name.index(to_someone)
            if to_someone == from_someone:
                final_msg1 = f"4you: {the_msg} (to yourself)"
                client_socket.send(final_msg1.encode())
            else:
                final_msg2 = f"4you: {the_msg} (to {to_someone})"
                client_socket.send(final_msg2.encode())
                clients_sockets_list[int(number)].send(final_msg.encode())

            print(str(number) + "\n")

        elif user_msg[0] == "0":
            break
        elif user_msg[0] == "5":
            pass
        else:
            reply = "false"
            client_socket.send(reply.encode())


def close_all_sockets():
    for client_socket in clients_sockets_list:
        client_socket.close()


def main():
    prime_num()
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen()

    print("Server is up and running")

    new_client_thread = Thread(target=lambda: new_client(server_socket))
    new_client_thread.start()
    input("to delete")

    close_all_sockets()
    server_socket.close()


if __name__ == "__main__":
    main()
