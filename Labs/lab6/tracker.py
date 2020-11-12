# File: tracker.py
# Author: Wameedh Mohammed Ali
# SID: 920678405
# Date: <the date when this file was last updated/created/edited>
# Description: this file contains the implementation of the tracker class.
import bencodepy
import socket
import threading
from torrent import *


class Tracker:
    """
    This class contains methods that provide implementations to support trackerless peers
    supporting the DHT and KRPC protocols
    """
    DHT_PORT = 12001

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
        # self._clienthandler = server.clienthandlers[0]
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("", self.DHT_PORT))
        self.non_broadcast_socket = None
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        self._routing_table = []

    def broadcast(self, message, self_broadcast_enabled=False):
        try:
            encoded_message = self.encode(message)
            self.udp_socket.sendto(encoded_message, ('<broadcast>', self.DHT_PORT))
            print("Message broadcast.....")
        except socket.error as error:
            print(error)

    def send_udp_message(self, message, ip, port):
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = self.encode(message)
            new_socket.sendto(message, (ip, port))
        except:
            print("error")

    def broadcast_listerner(self):
        try:
            print("Listening at DHT port: ", self.DHT_PORT)
            while True:
                raw_data, sender_ip_and_port = self.udp_socket.recvfrom(4096)
                if raw_data:
                    data = self.decode(raw_data)
                    ip_sender = sender_ip_and_port[0]
                    port_sender = sender_ip_and_port[1]
                    print("data received by sender", data, ip_sender, port_sender)
        except:
            print("Error listening at DHT port")

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
        # bc = bencodepy.Bencode('utf-8')
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
        # create the ping dictionary
        # pass the dictionary
        # ip = {'ip_address': self.host, 'port': self.port}
        # ping Query = {"t":"aa", "y":"q", "q":"ping", "a":{"id":"abcdefghij0123456789"}}
        id = self._torrent.info_hash()
        ping_Query = {"t": t, "y": y, "q": "ping", "a": {"id": id}}
        self.broadcast(ping_Query)

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

    def run(self, start_with_broadcast=True):
        """
        TODO: This function is called from the peer.py to start this tracker
        :return: VOID
        """
        if self._is_announce:
            threading.Thread(target=self.broadcast_listerner).start()
        else:
            print("This tracker does not support DHT protocol")

        if start_with_broadcast:
            # message = "Anyone listening in DHT port?"
            # self.broadcast(message, self_broadcast_enabled=True)
            self.ping("aa", "q")


# tracker = Tracker(None, Torrent("age.torrent"))
# tracker.run()
