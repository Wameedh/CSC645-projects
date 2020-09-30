########################################################################################################################
# Class: Computer Networks
# Date: 09/30/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Wameedh Mohammed Ali
# Student ID: 920678405
# Student Github Username: wameedh
# Lab Instructions: No partial credit will be given in this lab
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
import sys
from threading import Thread
from client_handler import ClientHandler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port = 12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: create the server socket
        self.client_handlers = {} # initializes client_handlers list

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            # your code here
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Listening at " + self.host + "/" + str(self.port))
        except socket.error as e:
            print("Error while listening for client %s" % e)
            self.serversocket.close()
            sys.exit(1)

    def threaded_client(self, clientsocket, addr):
        client_id = addr[1]
        client_handler = ClientHandler(self, clientsocket, addr)  # self is the server instance
        client_handler.run()  # inits all the components in client handler object
        #  adds the client handler object to the list of all the clients objects created by this server.
        #  key: client id, value: client handler
        client_handler.client_id = client_id  # assumes dict was initialized in class constructor


    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               clienthandler, addr = self.serversocket.accept()
               client_id = addr[1]
               self._send_clientid(clienthandler, client_id)
               Thread(target=self.threaded_client, args=(clienthandler, addr)).start()  # client thread started
            except socket.error as e:
               # handle exceptions here
               print("Error accepting client %s" % e)
               self.serversocket.close()
               sys.exit(1)

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        client_id = {'clientid': clientid}
        self.send(clienthandler, client_id)


    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)
        try:
            clienthandler.send(serialized_data)
        except socket.error as e:
            print("Error sending data %s" % e)
            self.serversocket.close()
            sys.exit(1)

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        try:
            data_from_client = clienthandler.recv(MAX_ALLOC_MEM)
        except socket.error as e:
            print("Error receiving data %s" % e)
            self.serversocket.close()
            sys.exit(1)
        if len(data_from_client) == 0:
            return None
        return pickle.loads(data_from_client)

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()











