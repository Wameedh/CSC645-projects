# File: tracker.py
# Author: <your name here>
# SID: <your student id here>
# Date: <the date when this file was last updated/created/edited>
# Description: this file contains the implementation of the tracker class.

import bencodepy

class Tracker:
    """
    This class contains methods that provide implementations to support trackerless peers
    supporting the DHT and KRPC protocols
    """

    def __init__(self, server, torrent, announce=True):
        """
        TODO: Add more work here as needed.
        :param server:
        :param torrent:
        :param announce:
        """
        self._server = server
        self._torrent = torrent
        self._is_announce = announce
        self._clienthandler = server.clienthandlers[0]
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        self._routing_table = []

    def encode(self, message):
        """
        bencodes a message
        :param message: a dictionary representing the message
        :return: the bencoded message
        """
        return bencodepy.encode(message)


    def decode(self, bencoded_message):
        """
        Decodes a bencoded message
        :param bencoded_message: the bencoded message
        :return: the original message
        """
        return bencodepy.decode(bencoded_message)



    def ping(self, t, y, a=None, r=None):
        """
        TODO: implement the ping method
        :param t:
        :param y:
        :param a:
        :return:
        """
        """
        TODO: implement the ping method. 
        :return:
        """
        pingQuery = {"t": t, "y": y, "q": "ping", "a": a, "r": r}
        data = self.encode(pingQuery)
        self._server.send(data)


    def find_node(self, t, y, a=None, r=None):
        """
        TODO: implement the find_node method
        :return:
        """
        pass

    def get_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the get_peers method
        :return:
        """
        pass

    def announce_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the announce_peers method
        :return:
        """
        pass

    def process_query(self):
        """
        TODO: process an incoming query from a node
        :return: the response
        """
        pass

    def send_response(self):
        """
        TODO: send a response to a specific node
        :return:
        """
        pass

    def run(self):
        """
        TODO: This function is called from the peer.py to start this tracker
        :return: VOID
        """
        pass


