"""
    Done by: BALIJAPELLY PRANAV   
"""
############################################################################################
""" SERVER PROGRAM"""
############################################################################################
from socket import *
from threading import Thread
import datetime
# creating a socket
server=socket(AF_INET,SOCK_STREAM)
#specifing ip address and port number for establishing server socket
host_ip='localhost'
port = 44444
server.bind((host_ip,port))# bind it to a host ip and a port
# start listening for TCP connections made to this socket
# the argument "1" is the max number of queued up clients allowed
server.listen(1)

clients=[]                      #creatinf empty list for storing client informaton
nicknames=[]                    #creating empty list for storing client names
thread_count=0
"""Function Description:This fuction sends(broadcasts) response to each client(other than who messaged) that are connected to this server
   Input: message to be sent and client who sent message to server
   Output: None"""
def Broadcast_message(data,client):
    for i in clients:
        if i!=client:
            i.send(data)
"""Function Description:Whenever connection is intialised between client and server, server calls this function to accepts request multiple times from client. 
   Input: client 
   Output: None"""   
def client_connection(client):
    while True:
        data=client.recv(1024)      #receives data from client
        check=data.decode()
        index=clients.index(client)
        name_str=nicknames[index]
        check=check[len(name_str)+1:]
        check=check.strip()
        if check!='quit':           #if data is other than quit then message is broadcates using above function
            Broadcast_message(data,client)
        else:                       #if data is quit, then client connection is closed and client info is removed from list.
            client.send("quit".encode('utf-8'))
            nickname=nicknames.pop(clients.index(client))
            clients.remove(client)          #client is removed from clients list
            client.close()                  #connection is closed
            time=datetime.time() 
            thread_count-=1
            #whenever a client connection is closed a broadcast message is sent which tells particular client had left.
            Broadcast_entry_exit(f'Server: time={time} {nickname} has left. Member count={thread_count}'.encode('utf-8'))
            break
"""Function Description:This fuction sends(broadcasts) response to each client(other than who messaged) that are connected to this server
                        whenever a new client joins or previous clients exits.
   Input: message to be sent.
   Output: None"""
def Broadcast_entry_exit(data):
    for i in clients:
        i.send(data)
while True:
    connection_socket,addr=server.accept()  #server accepts connection
    clients.append(connection_socket)       #client info is appended to list
    thread_count+=1                         #thread count is increased
    name=connection_socket.recv(1024)       #collecting client name
    nicknames.append(name.decode())         #adding client name to nickname list
    time=datetime.datetime.now()    
    time=time.strftime("%H:%M:%S")
    name=name.decode()
    #since new client has come broadcast message is been sent.
    Broadcast_entry_exit(f'Server: time={time} {name} has joined. Member count={thread_count}'.encode('utf-8'))
    thread=Thread(target=client_connection,args=(connection_socket,))   #aparitcular thread opens for each client
    thread.start()      #thread is started here



############################################################################################
############################################################################################
""" CLIENT PROGRAM """
############################################################################################
############################################################################################

from socket import *
import threading         
import sys
client=socket(AF_INET,SOCK_STREAM)#we are going to use TCP so second argument is SOCK_DSRAM
# These are server ip address and port which clients needs to know.
host_ip='localhost'
port=44444
client.connect((host_ip,port)) #client connects to server
"""Function Description:This function takes input from user and sends it to server. user may give any number of inputs he want, if user gives 
                        'quit' as input then loop breaks and exits from function
    Input: None
    Output: None
"""
def thread_query():
    print("Enter login name:")
    nickname=input()
    client.send(nickname.encode('utf-8'))
    while True:
        message=input()
        client.send(f'{nickname}: {message}'.encode('utf-8'))
        if message=='quit':
        	sys.exit()
        	break
"""Function Description:This function runs a infinite loop which goes on accepting requests from server until user gives 'quit' as input
    Input: None
    Output: None
"""
def thread_response():
    while True:
        data=client.recv(1024)          #message is received from server
        if (data.decode()=='quit'):     #if response from server is quit then thread is closed gets exited from function
        	sys.exit()
        	client.close()
        	break
        else:
        	print(data.decode())    #else message is printed
#To run both the functions parallelly threading is used here 
Response = threading.Thread(target=thread_response)     # thread_response function is given to a thread here
Response.start()                                        # thread start here
Query= threading.Thread(target=thread_query)            # thread_response function is given to a thread here
Query.start()                                           # thread start here







