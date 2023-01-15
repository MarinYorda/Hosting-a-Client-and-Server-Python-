# client.py

import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 1984 #port used by server
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    n = 0
    while n != 8:
        print("Python DB Menu \n")
        print("1. Find customer")
        print("2. Add customer")
        print("3. Delete customer")
        print("4. Update customer age")
        print("5. Update customer address")
        print("6. Update customer phone")
        print("7. Print report")
        print("8. Exit\n")
        n = (input("Select: "))

        if n in ['1', '2', '3', '4', '5', '6', '7', '8']:
            n = int(n)
        else:
            print("Invalid input, please try again! \n")

        if n == 1:
            name = input("find Customer Name: ")
            name = name.strip()
            send = str(n) + " " + name
            client.send(send.encode(FORMAT))
        elif n == 2:
            my_contact = input("Enter the customer information in the following format: name|age|address|phone number\n")
            send = str(n) + " " + my_contact
            client.send(send.encode(FORMAT))
        elif n == 3:
            name = input("Customer Name: ")
            name = name.strip()
            send = str(n) + " " + name
            client.send(send.encode(FORMAT))
        elif n == 4:
            name = input("Customer Name: ")
            name = name.strip()
            age = input("Please indicate the new age: ")
            send = str(n) + " " + name + "|" + age
            client.send(send.encode(FORMAT))

        elif n == 5:
            name = input("Customer Name: ")
            name = name.strip()
            address = input("Please indicate the new address: ")
            send = str(n) + " " + name + "|" + address
            client.send(send.encode(FORMAT))
        elif n == 6:
            name = input("Customer Name: ")
            name = name.strip()
            phone = input("Please indicate the new phone number: ")
            send = str(n) + " " + name + "|" + phone
            client.send(send.encode(FORMAT))
        elif n == 7:
            send = str(n) + " "
            client.send(send.encode(FORMAT))
        elif n == 8:
            print("Good bye")
            send = str(n) + " "
            client.send(send.encode(FORMAT))
            client.close()
            exit()

        if n in range(0, 9):
            result = client.recv(SIZE).decode(FORMAT)
            print(result)


if __name__ == '__main__':
    main()








