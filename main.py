from eleicao2017 import *
from node import *
import sys


def main():
	#node = Node()
	node_number = read_node_number()

	if(node_number is None  or (node_number not in range(0, N_NODES))):
		print "Erro ao ler numero do nodo atual!"
		return
	node = Node(node_number, NODES[node_number][0], NODES[node_number][1])
	node.bind_socket()

	for id, address in NODES.iteritems():
		if(node.id != id):
			print "port:{0} port:{1}".format(address[0], address[1])
			node.connect(id, address[0], address[1])

	#TODO: Mudar para verificar o IP de cada nodo que se conectou comigo e entao eu me conecto com o nodo do IP correspondente
	while len(node.nodes_alive) < N_NODES - 1:
		node.socket.listen(1)
		conn, addr_remote_socket = node.socket.accept()
		for id, address in NODES.iteritems():
			if(address[0] == addr_remote_socket[0]):
				node.add_node_alive(id, addr_remote_socket[0], addr_remote_socket[1], conn)
				break

		print "conn{0} -- addr{1}".format(conn, addr_remote_socket)

def read_node_number():
	if len(sys.argv) != 2:
		return None
	return int(sys.argv[1])	

main()
