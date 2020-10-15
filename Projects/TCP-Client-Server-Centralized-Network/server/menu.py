#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu(client) # creates object
#
########################################################################################

class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self, client):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = client


    def get_menu(self):
        """
        TODO: Inplement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Send a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = "\n****** TCP Message App ******\n\
-----------------------\n\
Options Available:\n\
1. Get user list\n\
2. Send a message\n\
3. Get my messages\n\
4. Create a new chat room\n\
5. Join an existing chat room\n\
6. Disconnect from server\n"

        return menu


