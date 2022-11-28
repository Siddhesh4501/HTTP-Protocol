from socket import *
from _thread import *
from Value import maxConnection
from HttpMethods import GET,HEAD,POST,PUT,DELETE

server=socket(AF_INET,SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
IP_addr="0.0.0.0"
port=8000
server.bind((IP_addr,port))
server.listen(10)


def remove(client):
    if client in list_of_clients:
        list_of_clients.remove(client)


def clientThread(conn,addr):
    print("Connection Established")
    print(addr)
    clientIp=addr[0]
    clientPort=addr[1]
    conn.settimeout(5)
    while 1:
        try:
            message=conn.recv(1048576).decode('ISO-8859-1')
            data=message.split("\r\n\r\n")[0]
            reqheader=data.split("\r\n")[0]
            if "GET" in reqheader:
                print("In get")
                get_reponse=GET(message)
                conn.send(get_reponse.encode())
            elif "HEAD" in reqheader:
                get_reponse=HEAD(message)
                conn.send(get_reponse.encode())
            elif "POST" in reqheader:
                get_reponse=POST(message)
                conn.send(get_reponse.encode())
            elif "PUT" in reqheader:
                get_reponse=PUT(message)
                conn.send(get_reponse.encode())
            elif "DELETE"  in reqheader:
                get_reponse=DELETE(message)
                conn.send(get_reponse.encode())
        except:
            conn.close()


list_of_clients=[]

while True:
    while len(list_of_clients)<maxConnection:
        conn,addr=server.accept()
        list_of_clients.append(conn)
        start_new_thread(clientThread,(conn,addr))
        list_of_clients.remove(conn)

    