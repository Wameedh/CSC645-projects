#######################################################################
# File:             client_helper.py
# Author:           Wameedh Mohammed Ali
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Client_helper class. This class manages the process of communicating between the server and the clinet
#                   When the client is interaction with menu options that has been sent from the server when the client joins
# Running:          Python 2: python client.py
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
import threading

class ClientHelper(object):

    def __init__(self,clientSocket ,client_id, client_name):
        """
        Class constractpr
        """
        self.clientSocket = clientSocket
        self.data = None
        self.client_id = client_id
        self.client_name = client_name
        self.print_lock = threading.Lock()  # creates the print lock

    def get_and_print_menu(self):
        """
        This mesthod would print the menu then it would prompt the user for input to interact with the menu options
        """
        if 'menu' in self.data: # check that the data coming from the server has the menu
            self.print_payload(self.data, 'menu') # print put the menu
            self.take_user_input() # prompt the suer for an input then process the input

    def take_user_input(self):
        """
        This method prompt the user for an input of an option form the menu
        then send that option to the server so that a response would be sent back so that it get processed
        """

        option = input("Your option <enter a number>: ")
        try:
            option = int(option)
            data = {'option_selected': option}
        except:
            print("Invalid option! Option need to be an integer and from 1 to 6!")
            data = {'option_selected': 0}

        if 1 > option > 6:
            print("Invalid option! Option need to be an integer and from 1 to 6!")

        if option == 2:
            message = input("Enter your message: ")
            recipient_id = input("Enter recipient id: ")
            data.update({'payload': message, 'recipient_id': recipient_id, 'sender_id': self.client_id})
        if option == 4:
            room_id = input("Enter new chat room id: ")
            data.update({'room_id': room_id, 'sender_id': self.client_id, 'client_name': self.client_name,
                         'chat_is_active': True})
        if option == 5:
            room_id = input("Enter chat room id to join: ")
            data.update({'room_id': room_id, 'sender_id': self.client_id, 'client_name': self.client_name,
                         'chat_is_active': True})
        self.send(data)

    def print_payload(self, data, key='payload'):
        """
        This method takes a dic and a key then it would print data Associated with the key from the dic
        Note that if no key has been passed the default would be 'payload'
        """
        payload = data[key]
        self.print_lock.acquire()
        print(payload)
        self.print_lock.release()

    def process(self, data):
        """
            This meothod would process the data after the client has sent an option choice to the server then
            the server has sent a respond with the data
        """
        self.data = data
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6:  # validates a valid option selected
            option = data['option_selected']

            """
                For option 1 to 3 we just need to print the payload coming from the server
            """
            self.print_payload(self.data)

            if option == 4:
                try:
                    client_id = data['sender_id']
                    client_name = data['client_name']
                    chat_is_active = data['chat_is_active']
                    self.creat_chatroom(client_id, client_name, chat_is_active)
                except KeyError as e:
                    print("Key error occurred while getting " + e)
            elif option == 5:
                try:
                    client_id = data['sender_id']
                    client_name = data['client_name']
                    room_id = data['room_id']
                    chat_is_active = data['chat_is_active']
                    self.join_chatroom(client_id, client_name, room_id, chat_is_active)
                except KeyError as e:
                    print("Key error occurred while getting " + e)
            elif option == 6:
                self.clientSocket.close()
        self.get_and_print_menu()

    def creat_chatroom(self, client_id, client_name, chat_is_active):

        while chat_is_active:
            data = self.receive()
            self.print_payload(data)

            chat_is_active = data['chat_is_active']

            user_input = input(self.client_name + ": ")
            message = str(self.client_name) + ": " + user_input

            data.update({'payload': message, 'client_name': client_name, 'client_id': client_id})

            if user_input == 'exit':
                chat_is_active = False

            if not chat_is_active:
                data.update({'option_selected': None, 'payload': user_input, 'chat_is_active': False})
            self.send(data)

    def join_chatroom(self, client_id, client_name, room_id, chat_is_active):

        while chat_is_active:
            user_input = input(self.client_name + ": ")

            if user_input == 'bye':

                chat_is_active = False

            if not chat_is_active:
                data = {'option_selected': None, 'payload': user_input, 'client_name': client_name,
                             'client_id': client_id, 'chat_is_active': True}
                self.send(data)

            if chat_is_active:
                message = str(self.client_name) + ": " + user_input
                data = {'payload': message, 'room_id': room_id, 'client_name': client_name, 'client_id': client_id, 'chat_is_active': True}
                self.send(data)

                data = self.receive()
                chat_is_active = data['chat_is_active']

                if chat_is_active:
                    self.print_payload(data)
                else:
                    print("The chat-room has been closed by the owner")

                    self.send({'chat_is_active': False})

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data)  # serialized data
        try:
            self.clientSocket.send(data)
        except socket.error as e:
            print("Error sending data %s" % e)
            self.clientSocket.close()

    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientSocket.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data