import socket
from threading import *
import RSA
from RSA import *
import random
import re

public_k = 0
private_k = 0
PORT = 7727
clients_sockets_list = []
clients_threads = []
users_name = []
public_keys_list = []


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
    global public_k, public_keys_list
    while True:

        user_msg = client_socket.recv(4096).decode()
        check = True
        if user_msg[0] == "1":
            user_msg = user_msg[1:]

            user_name = " ".join(user_msg.split()[0])
            user_name = re.sub(r'\s+', '', user_name)
            key_of_user = " ".join(user_msg.split()[1:])
            key_of_user = re.sub(r'\s+', '', key_of_user)
            key_of_user = key_of_user.replace("(", "")
            key_of_user = key_of_user.replace(")", "")

            try:
                res1 = tuple(map(int, key_of_user.split(',')))
            except ValueError:
                res1 = ""
                public_keys_list.append(res1)
            if user_name in users_name:
                check = False
            elif user_name == "":
                check = False
            else:
                users_name.append(user_name)
                public_keys_list.append(res1)

            if check:
                reply = f"0next {public_k}"
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
            user_msg = user_msg.replace("[", "")
            user_msg = user_msg.replace("]", "")

            um_list = list(user_msg.split(","))

            try:
                um_list = list(map(int, um_list))

            except TypeError:
                um_list = [25, 15]

            user_msg = decrypt(private_k, um_list)
            from_name = " ".join(user_msg.split()[0])
            from_someone = re.sub(r'\s+', '', from_name)

            to_name = " ".join(user_msg.split()[1])
            to_name = " ".join(user_msg.split()[1])
            to_someone = re.sub(r'\s+', '', to_name)
            msg = " ".join(user_msg.split()[2:])
            the_msg = msg

            number = users_name.index(to_someone)
            number2 = users_name.index(from_someone)

            if to_someone == from_someone:
                final_msg1_e = encrypt(public_keys_list[int(number)], f"you: {the_msg} (to yourself)")
                final_msg1 = f"4{final_msg1_e}"
                client_socket.send(final_msg1.encode())
            else:
                final_msg2_e = encrypt(public_keys_list[int(number2)], f"you: {the_msg} (to {to_someone})")
                final_msg2 = f"4{final_msg2_e}"
                client_socket.send(final_msg2.encode())
                final_msg3_e = encrypt(public_keys_list[int(number)], f"{from_someone}: {the_msg}")
                final_msg = f"3{final_msg3_e}"

                clients_sockets_list[int(number)].send(final_msg.encode())

        elif user_msg[0] == "0":
            user_msg = user_msg[1:]
            counter = users_name.index(user_msg)
            clients_sockets_list.pop(int(counter))
            clients_threads.pop(int(counter))
            users_name.pop(int(counter))
            public_keys_list.pop(int(counter))
            client_socket.close()

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
    input("to delete\n")

    close_all_sockets()
    server_socket.close()


if __name__ == "__main__":
    main()
