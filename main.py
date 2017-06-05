#!coding:utf-8
from eleicao2017 import *
from node import *
import sys

from threading import Timer



def main():
	#node = Node()
	node_number = read_node_number()

	#lê nodo id do argv
	if(node_number is None  or (node_number not in range(0, N_NODES))):
		print "{0}Erro ao ler numero do nodo atual!{1}".format(bcolors.FAIL, bcolors.ENDC)
		return
	#incializa nodo atual
	node = Node(node_number, NODES[node_number][0], NODES[node_number][1])
	node.bind_socket()

	#Tenta se conectar com os demais nodos
	for id, address in NODES.iteritems():
		if(node.id != id):
			print "Tentado se conectar em IP:{0} port:{1}".format(address[0], address[1])
			if(node.connect(id, address[0], address[1])):
				print "{0}Conectado{1}".format(bcolors.OKGREEN, bcolors.ENDC)
			else:
				print "{0}Não conetado{1}".format(bcolors.FAIL, bcolors.ENDC)

	#Espera até que todos os nodos se conectem
	print "Esperando conexão de todos os nodos"
	while len(node.nodes_alive) < N_NODES - 1:
		node.socket.listen(1)
		conn, addr_remote_socket = node.socket.accept()
		for id, address in NODES.iteritems():
			if(address[0] == addr_remote_socket[0]):
				node.add_node_alive(id, addr_remote_socket[0], addr_remote_socket[1], conn)
				print "{2}Nodo {0} conectado: addr{1}{3}".format(id, addr_remote_socket, bcolors.OKGREEN, bcolors.ENDC)
				break
	print "{0}Todos os nodos se conectaram{1}".format(bcolors.OKGREEN, bcolors.ENDC)

	#envia o hearthbeat do nodo em tempos em tempos
	hearthbeat_sender(node)


	while True:
		#recebe mensagem dos outros nodos
		message_reciver(node)
                #print  node.nodes_alive.items()



def read_node_number():
	if len(sys.argv) != 2:
		return None
	return int(sys.argv[1])	

main()
