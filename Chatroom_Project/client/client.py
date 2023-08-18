# Created by: Jonas Ferguson
# Date:  March 6, 2023
# Description: A client for a multi-threaded socket chat application.

import socket, time, sys
from threading import Thread

SERVER_PORT = 17308
SERVER_IP = '127.0.0.1'

def login(msg):
    """login(msg) ensures that data is in the right format 
     before sending the message to the server"""
    split = msg.split(" ") # separate out command and user/pass

    try:
        split[1] == split[2] # check to make sure user and password are given
    except:
        print("Please use the form >login username password")
    else: # everything is good, message can be sent
        try:
            server.send(msg.encode())
        except:
            print("Could not communicate with server")


def newuser(msg):
    """newuser(msg) ensures that userID and password are present and in the proper length.
    It then sends the message to the server"""
    split = msg.split(" ") # separate out command and userID/password

    try:
        if (len(split[1]) >= 3 and len(split[1]) <= 32): #if userID is the proper length
            if (len(split[2]) >= 4 and len(split[2]) <= 8): #if password is the proper length
                try:
                    server.send(msg.encode())
                except:
                    print("Could not communicate with server")
            else:
                print("Passwords must be 4-8 characters")
        else:
            print("UserIDs must be 3-32 characters")
    except:
        print("Please use the form >newuser username password")


def send(msg):
    """send(msg) ensures that a message is the proper length and syntax.
     It then sends the message to the server"""
    if (len(msg) >= 1 and len(msg) <= 256): #if message is the proper length (space for the word send is allowed
        try:
            split = msg.split(" ", 2) # split into [send, all/userID, message]
            split[1] # to make sure this exists
            split[2] # ^
        except: # if they don't exist
            print("Make sure to use 'send all' or 'send userID'")
            return
        try:
            server.send(msg.encode())
        except:
            print("Could not communicate with server")
    else:
        print("Messages are restricted to 1-256 characters")


def who(msg):
    """who(who) sends the message to the server."""
    try:
        server.send(msg.encode())
    except:
        print("Could not communicate with server")


def listen_for_messages():
    """listen_for_messages() is intended to be run in a thread.
     It continuously listens for messages from the server, then prints them out"""
    while True:
        msg = server.recv(500).decode()
        print(msg)


# socket create
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Socket creation failed with error %s" %(err))

# socket connection
try:
    server.connect((SERVER_IP, SERVER_PORT))
except:
    print("Socket connection failed")

print("My chat room client. Version Two.")
# create a thread to listen for server messages
listener = Thread()
listener = Thread(target=listen_for_messages)
listener.daemon = True
listener.start()

while True: # constantly listens for user input
    msg = input()

    # when input is found, runs the proper function for the given command
    if(msg.startswith("login")):
        login(msg)
    elif(msg.startswith("newuser")):
        newuser(msg)
    elif(msg.startswith("send")):
        send(msg)
    elif(msg.startswith("who")):
        who(msg)
    elif(msg.startswith("logout")):
        server.send("logout".encode())
        time.sleep(1) # waits to receieve logout message from the server
        break
    else:
        print("Please enter a proper command.  Available commands are: login, newuser, send, who, logout")

server.close()