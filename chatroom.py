from lutherium.node import LutheriumNode
from random import randint

def event_manager(packet):
    if packet["type"] == "message":
        print(packet["data"])

selecting = True
while selecting:
    try:
        my_node = LutheriumNode("127.0.0.1", randint(5000, 6000), command_back=event_manager) # For real cases enter your dedicated/VPN IP (NEVER USE 0.0.0.0 FOR REAL TESTS)
        selecting = False
    except OSError:
        pass

my_node.start()

print("Welcome to the Lutherium chatroom\nUse /merge {host} {port} to merge to a network")

while True:
    inpl = input(f"Annonymous@{my_node.net_name} : > ")
    inp = inpl.split()
    if inpl.startswith("/"):
        inpl = inpl.removeprefix("/")
        if inpl.startswith("merge"):
            if len(inp) == 3:
                my_node.connect_with_node(inp[1], int(inp[2]))
            else:
                print("Syntax Invalid: /merge {host} {port}")
        elif inpl.startswith("peer"):
            my_node.print_connections()
    else:
        my_node.bounce_to_nodes(my_node.package("message", inpl, my_node.generate_badge()))