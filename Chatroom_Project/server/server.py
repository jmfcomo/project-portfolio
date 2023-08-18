# Created by: Jonas Ferguson
# Date: March 6, 2023
# Description: A server for a multi-threaded socket chat application.

import socket, time
from threading import Thread

SERVER_PORT = 17308
SERVER_IP = '127.0.0.1'
MAXCLIENTS = 3

def listen_for_messages(clientSocket):
    """listen_for_messages() runs in a thread.  It listens to incoming messages
     from the open socket, and then calls other functions based on message contents"""
    
    username = "" # the currently logged in user, blank if not logged in
    while True: # listens forever
        try:
            msg = clientSocket.recv(300).decode() # listen to the socket
        except:
            print("Not connected to server")
            clientSockets.remove(clientSocket)

        #look through all the possible commands, and execute them when found
        if msg.startswith("login"):
            username = login(msg, username, clientSocket)

        if msg.startswith("newuser"):
            newuser(msg, username)

        if msg.startswith("send"):
            send(msg, username, clientSocket)

        if msg.startswith("who"):
            who(clientSocket)

        if msg.startswith("logout"):
            username = logout(username, clientSocket)


def login(msg, username, clientSocket):
    """login(msg, username, clientSocket) takes a userID and a password argument (separated by spaces after login)
    It checks the datafile to see if the userID and password pair is recognized
    If so, it sents the username to the now logged on user"""
    if (username != ""): # if already logged in
        try:
            clientSocket.send("You are already logged in".encode())
        except:
            print("Could not communicate with client")
        return
    split = msg.split(" ") #separate out arguments
    for user in users:
        if (user["userID"] == split[1]): #if userID is found
            if (user["password"] == split[2]): #if password matches expected password
                if split[1] in usernames:
                    try:
                        clientSocket.send("User already logged in on other client".encode())
                    except:
                        print("Could not communicate with client")
                    return ""
                #login has occurred
                print(split[1] + " login.")
                usernames[split[1]] = clientSocket #save username for all threads to see
                try:
                    clientSocket.send("login confirmed".encode()) #confirmation to current thread
                    for cs in clientSockets:
                        if not (cs == clientSocket): # all other threads
                            cs.send((split[1] + " joins.").encode())
                except:
                    print("Could not communicate with client")

                return split[1] #returns new username
            
    # userID was not found or password didn't match        
    try:        
        clientSocket.send("Denied. User name or password incorrect.".encode())
    except:
        print("Could not communicate with client")
    return "" # ensures username is still blank
    

def newuser(msg, username):
    """newuser(msg, username) takes a userId and a password argument (separated by spaces after login)
    It checks to see if the user is already logged in.
    If not, it checks to see if the given userID already exists.
    If not, it adds the new userID and password pair to the database and file of known users."""

    split = msg.split(" ") #separate out arguments
    # print("Username is" + username) REMOVE
    if (username != ""): #if already logged in
        try:
            clientSocket.send("A new user may not be created while logged in.".encode())
        except:
            print("Could not communicate with client")
        return
    
    for user in users:
        if (user["userID"] == split[1]): #if given userID already exists
            try:
                clientSocket.send("Denied. User account already exists.".encode())
                return
            except:
                print("Could not communicate with client")
    
    users.append({'userID': split[1], 'password': split[2]}) # adds userID/password pair to temporary user database
    
    try:
        with open('users.txt', 'a') as userFile:
            userFile.write("\n(" + split[1] + ", " + split[2] + ")") #writes the pair to the file
    except:
        print("Could not write new user to file")

    try:
        clientSocket.send("New user account created. Please login.".encode())
    except:
        print("Could not communicate with client")
    print("New user account created.")


def send(msg, username, clientSocket):
    """send(msg, username, clientSocket) recieves a message from the client.
     It first ensures that the user is logged in.
     If it is a send all message, the message is sent back to all connected clients,
        except the one that send the message.
     If it is a send UserID message, then the message is sent to the specified user."""
    
    if (username == ""): # if not logged in
        try:
            clientSocket.send("Denied. Please login first.".encode())
        except:
            print("Could not communicate with client")
        return
    split = msg.split(" ", 2) # breaks apart msg into [send, all/userID, message]
    if (split[1] == "all"): #send all message
        for client in clientSockets:
            if not (client == clientSocket): # all other clients
                try:
                    client.send((username + ": " + split[2]).encode()) # send message out to client
                except:
                    print("Could not communicate with client")
        print(username + ": " + split[2])
        return
    else: # send UserID message
        for user in usernames.keys(): # looks through all logged in users
            if (user == split[1]): #if userID matches
                try:
                    usernames[user].send((username + ": " + split[2]).encode()) # send message to that user
                except:
                    print("Could not communicate with client")
                print(username + " (to " + user + "): " + split[2])
                return
    # userID not found
    try:
        clientSocket.send("Could not find specified user".encode())
    except:        
        print("Could not communicate with client")
    print("user not found")
        

def who(clientSocket):
    """ who(clientSocket) takes no arguments from the user
        It sends the client a list of the currently online users."""
    userlist = ""
    for user in usernames:
        userlist += user + ", " #adds each user to a list
    userlist = userlist[:-2] # remove trailing comma
    try:
        clientSocket.send(userlist.encode())
    except:
        print("Could not communicate with client")


def logout(username, clientSocket):
    """logout(username, clientSocket) logs out the current user.
    It first checks to make sure that the user is not already logged out.
    If so, it sends a message to the clients saying who has logged out.
    It then updates the current user back to blank"""

    if (username == ""): # if already logged out
        try:
            clientSocket.send("You are already logged out.".encode())
        except:
            print("Could not communicate with client")
        return ""
    
    try:
        clientSocket.send((username + " left.").encode()) # sends logout message to client
    except:
        print("Could not communicate with client")
    print(username + " logout.")
    usernames.pop(username) # remove username from logged in users
    clientSockets.discard(clientSocket) #remove socket from list
    time.sleep(2)
    exit() #terminate thread


# file opening
try:
    users = [] #defines the list that will hold userID/password pairs
    userFile = open('users.txt', 'r', encoding="utf-8")
except:
    open("users.txt", 'x') # creates the data file, if it doesn't already exist
else:
    # read in file data
    try:
        for line in userFile:
            splitLine = line.split(", ") # breaks apart 
            splitPass = splitLine[1].split(")") # explicity removes closing ')' as some lines end in '\n', others don't
            users.append({'userID': splitLine[0][1:], 'password': splitPass[0]}) #adds the extracted userID/pass values
        userFile.close()
    except:
        print("The userfile cannot be properly read.")

# socket create
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error as err:
    print("Socket creation failed with error %s" %(err))

# socket bind
try:
    server.bind((SERVER_IP, SERVER_PORT))
except:
    print("Socket binding failed")

# socket listen
try:
    server.listen()
except:
    print("Socket listen failed")

print("My chat room server. Version Two.")

clientSockets = set() # will hold each connected client
usernames = dict() # will hold key:value dict pairs of userID:client

while True:
    clientSocket, address = server.accept()
    if len(clientSockets) < MAXCLIENTS: # checks if max clients have been exceeded
        clientSockets.add(clientSocket) # added to list of active sockets
        # create a thread to listen for messages
        listener = Thread()
        listener = Thread(target=listen_for_messages, args=(clientSocket,))
        listener.daemon = True
        listener.start()
    else: #too many clients logged in
        try:
            clientSocket.send("There are already the maximum number of clients logged in.".encode())
        except:
            print("Could not communicate with client")

for clientSocket in clientSockets:
    clientSocket.close()
server.close()