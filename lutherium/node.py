from p2pnetwork.node import Node as BaseNode
from random import randint


class LutheriumNode(BaseNode):
    conn_port = 0

    network = { # If people are conntecting to you your network is being determined by this genesis
        "network": {
            "about": "This was the first contract signed in the Network Database"
        }
    }
    
    net_name = "Lutherium Service Network"
    seen_badges = [0]
    started = True
    synced = False

    @staticmethod
    def command_back_ex(packet):
        print(f"{packet['type']} | {packet['data']}")

    command_back = command_back_ex

    def __init__(self, host, port, id=None, callback=None, command_back=None):
        print(f"Welcome to the {self.net_name} network! You first have to connect to a node or act as a genesis node.")
        super(LutheriumNode, self).__init__(host, port, id, callback, 0)
        self.conn_port = port
        if command_back != None:
            self.command_back = command_back
    
    def generate_badge(self):
        x = 0
        while x in self.seen_badges:
            x = randint(111111111111, 999999999999)
        return x

    @staticmethod
    def package(type, data, badge):
        """
        Package data to a specific format
        """
        return {
            "type": type,
            "data": data,
            "badge": badge
        }

    def set_subnet(self, name : str):
        """
        Set network name
        """
        self.net_name = name

    def bounce_to_nodes(self, package):
        """
        Bounce data to Nodes in the network
        """
        self.seen_badges.append(package["badge"])
        self.send_to_nodes(package)

    def announce_self(self):
        self.bounce_to_nodes(self.package("new_node", [self.host, self.port], badge=self.generate_badge()))

    def outbound_node_connected(self, connected_node):
        print("Outbound Node connected --> " + connected_node.id[:8])
        if self.started:
            self.send_to_node(connected_node, self.package("network_sync", "REQUEST_NETWORK_INFO", self.generate_badge()))
            print("Syncing with network...")
            self.announce_self()
            self.started = False
        
    def inbound_node_connected(self, connected_node):
        print("Inbound Node connected <-- " + connected_node.id[:5])

    def inbound_node_disconnected(self, connected_node):
        print("Inbound Node disconnected <X> " + connected_node.id[:5])

    def outbound_node_disconnected(self, connected_node):
        print("Outbound Node disconnected <X> " + connected_node.id[:5])

    def node_message(self, connected_node, data):
        package = data

        if package["type"] == "network_sync":
            self.send_to_node(connected_node, self.package("resync", {"network": self.network, "generated_badges": self.seen_badges, "net_name": self.net_name}, self.generate_badge()))
        elif package["type"] == "resync":
            if not self.synced:
                print("Syncing with Genesis... ")
                self.network = package["data"]["network"]
                self.seen_badges = package["data"]["generated_badges"]
                self.net_name = package["data"]["net_name"]
                print("Sync Confirmed")
                self.synced = True
            else:
                print("Genesis can only give past network data")

        elif not package["badge"] in self.seen_badges:
            self.seen_badges.append(package["badge"])
            self.send_to_nodes(package)
            print("My Network Peer <-- Bouncing... --> My Network")

            if package["type"] == "new_node":
                # This contains a array [host, port]
                host = package["data"]
                my_host = [self.host, self.port]
                if host != my_host:
                    print("Conecting to new Node")
                    self.connect_with_node(host[0], host[1])
            
            else:
                self.command_back(package)

        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("Node is disconnecting to Outbound node <X> " + connected_node.id)
        
    def node_request_to_stop(self):
        print("Node requested to stop")
