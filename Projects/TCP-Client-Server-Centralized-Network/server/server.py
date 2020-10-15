#######################################################################
# File:             server.py
# Author:           Wameedh Mohammed Ali
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Server class. This class manages the connections
#                   and creat thread for each client who joins the network
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import threading
from builtins import object
import socket
import pickle
from client_handler import ClientHandler

class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, host='127.0.0.1', port=5000):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {} # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        self.chatrooms = {}  # dictionary of chatrooms objects. format {room_id: chatroom_object}
        self.host = host
        self.port = port
        # TODO: bind the socket to a public host, and a well-known port
        self.serversocket.bind((self.host, self.port))
        # race condition locks
        self.clients_update_lock = threading.Lock()
        self.send_client_id_lock = threading.Lock()
        self.send_and_receive_data_from_client_lock = threading.Lock()

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        #TODO: your code here
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Listening at " + self.host + "/" + str(self.port))
        except socket.error as e:
            print("Error while listening for client %s" % e)
            self.serversocket.close()

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # TODO: Accept a client
                # TODO: Create a thread of this client using the client_handler_threaded class
                clienthandler, addr = self.serversocket.accept()
                threading.Thread(target=self.client_handler_thread, args=(clienthandler, addr)).start()  # client thread started

            except socket.error as e:
                # TODO: Handle exceptions
                print("Error accepting client %s" % e)
                self.serversocket.close()

    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        try:
            self.send_and_receive_data_from_client_lock.acquire()
            serialized_data = pickle.dumps(data)
            clientsocket.send(serialized_data)
            self.send_and_receive_data_from_client_lock.release()

        except socket.error as e:
            print("Error sending data %s" % e)
            self.serversocket.close()

    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        try:
            self.send_and_receive_data_from_client_lock.acquire()
            data_from_client = clientsocket.recv(MAX_BUFFER_SIZE)
            data = pickle.loads(data_from_client)
            self.send_and_receive_data_from_client_lock.release()
            return data
        except socket.error as e:
            print("Error receiving data %s" % e)
            self.serversocket.close()

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        self.send_client_id_lock.acquire()
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)
        print("Client with client id " + str(id) + " has been connected to the server!")
        self.send_client_id_lock.release()

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        client_id = address[1]
        self.send_client_id(clientsocket, client_id)
        #TODO: create a new client handler object and return it
        client_handler = ClientHandler(self, clientsocket, address)
        name = self.receive(clientsocket)
        client_handler.name = name
        self.clients_update_lock.acquire()
        self.clients.update({client_id: client_handler}) # adding to dictionary of clients handlers objects
        self.clients_update_lock.release()
        client_handler.run()
        return client_handler

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()


