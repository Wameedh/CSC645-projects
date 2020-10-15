#######################################################################################
# File:             chatroom.py
# Author:           Wameedh Mohammed Ali
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      This class represents a chat room object that users can create. It stores
#                   a list of users connected to the chat room and the owner of the room info.
#                   It would also manages adding and removing users from the chat
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
# Usage :           chatroom = Chatroom(owner_name, owner_id, room_id)
#
########################################################################################

class Chatroom(object):

    """
    Object Chatroom represents a chatroom users can access.  A chatroom object has the following:
    - Owner id
    - Owner name
    - Room id
    - a list of users
    And three methods
    - add_user()
    - remove_user()
    - get_room_id()
    """

    def __init__(self, owner_name, owner_id, room_id):
        self.owner_id = owner_id
        self.room_id = room_id
        self.owner_name = owner_name
        self.users = {}

    def add_user(self, user_id, user):
        self.users.update({user_id: user})

    def remove_user(self, user_id):
        self.users.pop(user_id)

    def get_room_id(self):
        return self.room_id




