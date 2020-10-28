#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import datetime
import threading
from menu import Menu
from chatroom import Chatroom

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.run_status = True # changes to false when the client disconnects from the server
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.name = None #name of the client associated with this object
        self.menu_list = None # menu option would got from the menu object
        self.server = server_instance
        self.clientsocket = clientsocket

        self.message_lock = threading.Lock()
        self.print_lock = threading.Lock()  # creates the print lock
        self.access_chatrooms_list_lock = threading.Lock()

        self.unread_messages = [] # each client would have its own unread_messages when we create a thread.

    def _send_menu(self):
        """
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        data = {'menu': self.menu_list, 'option_selected': 7}
        self.send(data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        data = self.receive()
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6: # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                self._save_message(data)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                self._create_chat(data)
            elif option == 5:
                self._join_chat(data)
            elif option == 6:
                self._disconnect_from_server()
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        message = "Users in server:\n"
        clients_list = self.server.clients
        for user in clients_list:
            message += str(user) + " " + clients_list[user].name + "\n"

        data = {'option_selected': 1, 'payload': message}
        self.send(data)
        self.print_lock.acquire()
        print("Users list has been sent to " + str(self.client_id))
        self.print_lock.release()

    def _save_message(self, data):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        recipient_id = data['recipient_id']
        message = data['payload']

        message_received = False

        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M: ")
        message_to_be_saved = date_string + message + (" (from: %s)" % self.name)

        clients_list = self.server.clients

        for user in clients_list:
            if str(user) == recipient_id:
                self.message_lock.acquire()
                clients_list[user].unread_messages.append(message_to_be_saved)
                message_received = True
                self.message_lock.release()


        if message_received:   # Send feedback to user
            data.update({'option_selected': 2, 'payload': "Message sent!"})
            self.send(data)
            self.print_lock.acquire()
            print("Message has been saved in " + str(self.client_id) + " inbox!")
            self.print_lock.release()
        else:
            data.update({'option_selected': 2, 'payload': "Message sending failed!"})
            self.send(data)
            self.print_lock.acquire()
            print("Saving message in " + str(self.client_id) + " inbox failed")
            self.print_lock.release()

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        if not self.unread_messages:   # Alert user if they have no unread messages
            data = {'option_selected': 3, 'payload': "No unread messages!"}
            self.send(data)
            return
        messages = "My messages:\n"
        # taking care of race condition
        # in case another user is sending a message while we are reading from unread_messages
        self.message_lock.acquire()
        messages_list = self.unread_messages
        self.message_lock.release()
        for message in messages_list:
            messages += message + "\n"
        # Send messages
        data = {'option_selected': 3, 'payload': messages}
        self.send(data)

        self.message_lock.acquire()
        self.unread_messages.clear()
        print("Messages has been sent to client " + str(self.client_id))
        self.message_lock.release()

    def _create_chat(self, data):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param data:
        :return: VOID
        """
        room_id = data['room_id']
        owner_id = data['sender_id']
        owner_name = data['client_name']
        chat_is_active = data['chat_is_active']

        chat_room = Chatroom(owner_name, owner_id, room_id)

        self.access_chatrooms_list_lock.acquire()
        self.server.chatrooms.update({room_id: chat_room})
        self.access_chatrooms_list_lock.release()

        data.update({'option_selected': 4, 'room_id': room_id, 'payload': "----------------------- Chat Room " + str(room_id) + " ------------------------\nType 'exit' to close the chat room.\nChat room created by: " + owner_name + "\nWaiting for other users to join....\n"})
        self.send(data)

        chat_room = self.sign_in_to_chatroom(room_id)

        if chat_room == -1:
            payload = "Chat room " + room_id + " could not be created, please try again!"
            data.update({'payload': payload, 'chat_is_active': False})
            self.send(data)
            return

        while chat_is_active:
            data = self.receive()
            sender_id = data['client_id']

            if sender_id == chat_room.owner_id:
                chat_is_active = data['chat_is_active']
                if not chat_is_active:
                    self.server.chatrooms.pop(room_id)
                    data.update({'menu': self.menu_list})

            users = chat_room.users
            self.send_message_to_all_users(users, sender_id, data)

    def _join_chat(self, data):
        """
        TODO: join a chat in a existing room
        :param data:
        :return: VOID
        """
        room_id = data['room_id']
        chat_is_active = data['chat_is_active']


        chat_room = self.sign_in_to_chatroom(room_id)

        if chat_room == -1:
            payload = "Chat room " + room_id + " does not exist"
            data.update({'payload': payload, 'chat_is_active': False})
            self.send(data)
            return

        data.update({'option_selected': 5, 'room_id': room_id, 'payload': "----------------------- Chat Room " + str(
            room_id) + " ------------------------\nJoined to chat room " + str(
            room_id) + "\nType 'bye' to exit this chat room.", 'chat_is_active': True})
        self.send(data)

        while chat_is_active:
            data = self.receive()
            chat_is_active = data['chat_is_active']
            if not chat_is_active:
                break
            sender_id = data['client_id']
            message = data['payload']
            username = data['client_name']

            if message == "bye":
                user_leaving_chat_message = username + "  has left the chat.."
                data.update({'payload': user_leaving_chat_message})
                self.sign_out_of_chatroom(chat_room, sender_id)
                chat_is_active = False

            users = chat_room.users
            self.send_message_to_all_users(users, sender_id, data) # notify the chat that the user has left

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        self.server.clients.pop(self.client_id, 'No Key found')
        print(self.server.clients)
        self.run_status = False
        self.server_ip = None
        self.unread_messages = None
        self.name = None
        print("Client: %s disconnected" % self.client_id)
        self.client_id = None

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        self.delete_client_data()
        self.clientsocket.close()

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientsocket.recv(max_mem_alloc)
        try:
            data = pickle.loads(raw_data)
            return data
        except:  # create error message
            print("Listening failed!")
            #self._disconnect_from_server()

#----------------------------------------#
#         HELPER METHODS SECTION         #
#________________________________________#

    def get_element_from_list_on_server(self, list, element_id):
        """
        This method takes an list and an element id
        it will return the element from the list if found
        else it will return -1
        """
        element = list.get(str(element_id), "1")

        if element != "1":

            return element
        else:
            return -1  # returns -1 if element not found in the elements list

    def sign_in_to_chatroom(self, room_id):
        """
        this method takes a room id then it would sign-in the client to that room
        if chatroom does not exist
        the return value for get_element_from_list_on_server() is -1 would be returned from this method as well
        """
        chat_room = self.get_element_from_list_on_server(self.server.chatrooms, room_id)
        if chat_room != -1:
            chat_room.add_user(self.client_id, self)
        return chat_room

    def sign_out_of_chatroom(self, chat_room, client_id):
        """
        This method would remove the suer from the chat room users list
        """
        chat_room.remove_user(client_id)

    def send_message_to_all_users(self, users, sender_id, data):

        """
        This method would take user list sender id and data/message
        it would send the data to all users in the list but the sender won't get it
        """
        for user in users:
            if user != sender_id:
                users[user].send(data)

    def run(self):
        """
        Runs the Client Handler until user picks option 6
        :return: VOID
        """
        menu = Menu(self)
        self.menu_list = menu.get_menu()
        while self.run_status:
            self._send_menu()
            self.process_options()






