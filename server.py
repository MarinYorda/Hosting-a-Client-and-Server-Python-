# server.py

import socket


IP = socket.gethostbyname(socket.gethostname())
PORT = 1984  # port to liston on (non-priviledge ports > 1023)
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


class Contact:
    def __init__(self, name, age, address, phonenum) -> None:
        self.name = name
        self.int = age
        self.address = address
        self.phone = phonenum

    def setage(self, age) -> None:
        self.int = age

    def setaddress(self, address) -> None:
        self.address = address

    def setphone(self, phone) -> None:
        self.phone = phone

    def __repr__(self) -> str:
        return f"{self.name}|{self.int}|{self.address}|{self.phone}"


def find_customer(info, contacts):
    for x in contacts:
        if x.name == info:
            return str(x)
        print(info)
    return "find Customer was not found\n"


def update_age(contacts, name, age):
    for x in contacts:
        if x.name == name:
            x.setage(age)
            return "Customer " + str(x.name) + "'s age was updated."
    return "Customer was not found\n"


def update_address(contacts, name, address):
    for x in contacts:
        if x.name == name:
            x.setaddress(address)
            return "Customer " + str(x.name) + "'s address was updated."
    return "Customer was not found\n"


def update_phone(contacts, name, phone):
    for x in contacts:
        if x.name == name:
            x.setphone(phone)
            return "Customer " + str(x.name) + "'s phone was updated."
    return "Customer was not found\n"


def update_txt(contacts):
    f = open("data.txt", "w")
    for x in contacts:
        x = str(x) + "\n"
        f.write(x)
    f.close()


def main():
    print("[STARTING]Server is starting")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print("[LISTENING]Server is listening")

    f = open("data.txt", "r")
    count = 0
    contacts = []

    for x in f:
        count += 1
        x = x.strip()
        x = x.split('|')
        if len(x) != 4:
            continue
        for i in range(0, 4):
            x[i] = x[i].strip()
        if x[0] == "":
            continue
        contat = Contact(x[0], int(x[1]), x[2], x[3])
        contacts.append(contat)
        update_txt(contacts)

    f.close()

    conn, addr = s.accept()
    print(f"Connected by {addr}")
    conn.send("Data file has been accessed".encode(FORMAT))  # maybe remove

    while True:

        task = conn.recv(SIZE).decode(FORMAT)

        myinstruction = ()
        myinstruction = task.split(" ", 1)

        method = myinstruction[0]
        therest = myinstruction[1]

        if method == '1':
            msg = find_customer(therest, contacts)
            conn.send(msg.encode(FORMAT))
        if method == '2':
            new = therest.split('|')
            if len(new) != 4:
                msg = "Invalid input for new customer\n"

            else:
                new[0] = new[0].strip()
                if new[0] == "":
                    msg = "Invalid input for new customer\n"
                else:
                    for x in contacts:
                        if x.name == new[0]:
                            msg = "Customer already exists\n"
                            conn.send(msg.encode(FORMAT))

                    newcontact = Contact(new[0], int(new[1]), new[2], new[3])
                    contacts.append(newcontact)
                    update_txt(contacts)
                    msg = "Customer: " + str(newcontact) + " has been succesfully added\n"
            conn.send(msg.encode(FORMAT))

        if method == '3':
            i = 0
            deleted = False
            for x in contacts:
                if x.name == therest:
                    contacts.pop(i)
                    update_txt(contacts)
                    deleted = True

                i = i + 1
            deleted_msg = "delete Customer: " + therest + " has been removed\n"
            not_deleted_msg = "delete Customer does not exist\n"
            msg = deleted_msg if deleted else not_deleted_msg
            conn.send(msg.encode(FORMAT))

        if method == '4':
            new = ()
            new = therest.split("|")
            msg = update_age(contacts, new[0], new[1])
            update_txt(contacts)
            conn.send(msg.encode(FORMAT))

        if method == '5':
            new = ()
            new = therest.split("|")
            msg = update_address(contacts, new[0], new[1])
            update_txt(contacts)
            conn.send(msg.encode(FORMAT))

        if method == '6':
            new = ()
            new = therest.split("|")
            msg = update_phone(contacts, new[0], new[1])
            update_txt(contacts)
            conn.send(msg.encode(FORMAT))

        if method == '7':
            msg = "** Python DB contents **\n"
            contacts.sort(key=lambda p: p.name)
            for x in contacts:
                msg += str(x) + "\n"
            conn.send(msg.encode(FORMAT))

        if method == '8':
            conn.close()
            print(f"Disconnected from {addr}")
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            conn.send("Data file has been accessed".encode(FORMAT))


if __name__ == '__main__':
    main()


