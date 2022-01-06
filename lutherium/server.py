try:
    from lutherium.node import LutheriumNode
except:
    from node import LutheriumNode

PEER = ["0.0.0.0", 5001] # This is the origin server which should point to your CLI Server, select None if you dont need it

node = LutheriumNode("0.0.0.0", port=5000)

print("=== Server Lutherium Node ===")
print("Starting...")
node.start()

if PEER != None:
    print("Connecting to Genesis...")
    node.connect_with_node(PEER[0], PEER[1])
    print(node.print_connections())
    print(f"Working as {node.net_name}")
