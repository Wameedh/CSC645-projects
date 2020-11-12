# File: tracker.py
# Author: Wameedh Mohammed Ali
# SID: 920678405
# Date: <the date when this file was last updated/created/edited>
# Description: this file contains the implementation of the tracker class.

import time # for testing

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
        self._routing_table = [["127.0.0.1", 12002], ["127.0.0.1", 12003],  ["127.0.0.1", 12004]]




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
                    print(data)
                    self.process_query(data['q'], ip_sender, port_sender)
                    print("data received by sender", data, ip_sender, port_sender)
        except:
            print("Error listening at DHT port")

    def encode(self, message):
        """
        bencodes a message
        :param message: a dictionary representing the message
        :return: the bencoded message
        """
        bencode_message = bencodepy.encode(message)
        print("bencoded = ", bencode_message)
        return bencode_message

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
        encoded_id = self.get_encoded_ID()
        #hashed_id = self._torrent._hash_torrent_info(encoded_id)
        ping_Query = {"t": t, "y": y, "q": "ping", "a": {"id": encoded_id}}

        print("ping Query = ", ping_Query)
        self.broadcast(ping_Query)

    def get_encoded_ID(self):
        id = self._server.getID()
        return bencodepy.encode(id)

    def find_node(self, t, y, a=None, r=None):
        """
        TODO: implement the find_node method
        :return:
        """
        """
        find_node Query = {"t": "aa", "y": "q", "q": "find_node","a": {"id": "abcdefghij0123456789", "target": "mnopqrstuvwxyz123456"}}
        bencoded = d1:ad2: id20:abcdefghij01234567896: target20:mnopqrstuvwxyz123456e1: q9:find_node1: t2:aa1: y1:qe
        """
        encoded_id = self.get_encoded_ID()
        find_node_Query = {"t": t, "y": y, "q": "find_node","a": {"id": encoded_id, "target": ["127.0.0.1", 5000]}}
        print("find_node Query = ", find_node_Query)
        self.broadcast(find_node_Query)

    def get_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the get_peers method
        :return:
        """
        encoded_id = self.get_encoded_ID()
        get_peers_Query = {"t": t, "y": y, "q": "get_peers", "a": {"id": encoded_id, "info_hash": self._torrent.info_hash()}}
        print("get_peers Query = ", get_peers_Query)
        self.broadcast(get_peers_Query)


    def announce_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the announce_peers method
        :return:
        """
        encoded_id = self.get_encoded_ID()
        announce_peers_Query = {"t": t, "y": y, "q": "announce_peer", "a": {"id": encoded_id, "implied_port": 1, "info_hash": self._torrent.info_hash(), "port": 6881, "token": "aoeusnth"}}
        print("announce_peers Query = ", announce_peers_Query)
        self.broadcast(announce_peers_Query)

    def process_query(self, query, ip, prot):
        """
        TODO: process an incoming query from a node
        :return: the response
        """
        # id = query[b'a'][b'id']
        #
        # ip_address = id['a']['id']
        # port =
        encoded_id = self.get_encoded_ID()
        if query == 'ping':
            ping_response = {"t": "aa", "y": "q", "q": "ping", "a": {"id": encoded_id}}
            self.send_udp_message(ping_response, ip, prot)
        elif query == 'find_node':
            find_node_response = {"t": "aa", "y": "r", "r": {"id": encoded_id, "nodes": self._torrent.nodes()}}
            self.send_udp_message(find_node_response, ip, prot)
        elif query == 'get_peers':
            response_with_peers = {"t":"aa", "y": "r", "r": {"id": encoded_id, "token": "aoeusnth", "values": ["axje.u", "idhtnm"]}}
            self.send_udp_message(response_with_peers, ip, prot)
        elif query == 'announce_peers':
            response_announce_peers = {"t": "aa", "y": "r", "r": {"id": encoded_id}}
            self.send_udp_message(response_announce_peers, ip, prot)

    def run(self, start_with_broadcast=False):
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

            # TEST.....
            self.ping("aa", "q")
            time.sleep(2)
            self.find_node('aa', 'q')
            time.sleep(2)
            self.get_peers('aa', 'q')
            time.sleep(3)
            self.announce_peers('aa', 'q')

            # message = self.ping('aa', 'q')
            # self.broadcast(message, self_broadcast_enabled=True)
            #time.sleep(2)
            # message = self.find_node('aa', 'q')
            # self.broadcast(message, self_broadcast_enabled=True)
            # time.sleep(2)
            # message = self.get_peers('aa', 'q')
            # self.broadcast(message, self_broadcast_enabled=True)
            # time.sleep(1)
            # message = self.announce_peer('aa', 'q')
            # self.broadcast(message, self_broadcast_enabled=True)


# tracker = Tracker(None, Torrent("age.torrent"))
# tracker.run()
