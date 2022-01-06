try:
    from lutherium.node import LutheriumNode
except:
    from node import LutheriumNode

def main():
    print("Lutherium CLI, made for deploying projects")

    node_enabled = False

    running = True
    while running:
        inpl = input("Node@Lutherium : > ")
        inp = inpl.split()
        if inpl != "":
            if inp[0] == "connect":
                if len(inp)<3:
                    print("Not enough arguments: connect {host} {port}")
                elif not node_enabled:
                    print("Initialize node first using initialize")
                else:
                    node.connect_with_node(inp[1], int(inp[2]))
            elif inp[0] == "init":
                if len(inp)<3:
                    print("Not enough arguments: initialize {host} {port}")
                else:
                    node = LutheriumNode(inp[1], int(inp[2]))
                    node.start()
                    node_enabled = True
            elif inp[0] == "exit":
                if node_enabled:
                    node.node_request_to_stop()
                    node_enabled = False
                else:
                    print("Node not initialized")
            
            elif node_enabled:
                if inp[0] == "peers":
                    node.print_connections()
                elif inp[0] == "help":
                    print("Check docs")
                elif inp[0] == "announce":
                    if input("Your Node should already be capturing discoveries to others\nDo you want to bounce new node data out? (yes/no) >>>").lower().startswith("y"):
                        node.announce_self()
                elif inp[0] == "name":
                    node.set_subnet(inpl.removeprefix("name "))
                    print(f"Set name to {node.net_name}")
                elif inp[0] == "netname":
                    print(node.net_name)
                else:
                    node.bounce_to_nodes(node.package("message", inpl, node.generate_badge()))