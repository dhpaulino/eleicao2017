from bitarray import *
from threading import Timer
import socket

N_NODES=4
MSG_SIZE = 1 #numeros de bits
HEARTHBEAT_TIME = 5 #segundos
HEARTHBEAT_MAX_WAIT_TIME = 8
NODES={0: ("200.17.202.6", 5313), #macalan
 1: ("200.17.202.11", 5313), #mumm
 2: ("200.17.202.28", 5313), #orval
 3: ("10.254.223.52", 5313)} #h48


"""
ESTRUTURA DA MENSAGEM

|tipo(1 bit)|

TIPO
0 - hearthbeat
1 - ?
"""

#TODO: usar mesmo objeto timer sempre
def hearthbeat_sender(node):
	node.send_hearthbeat()
	t = Timer(HEARTHBEAT_TIME, hearthbeat_sender, [node])
	t.start()
def message_reciver(node):

	for id, other_node in node.nodes_alive.iteritems():
		try:
			msg = bitarray(MSG_SIZE)
			bitarray(other_node.socket.recv_into(msg))
			print "Recebido msg de {1}:{0}".format(msg, id)
		except socket.error, e:
			pass
def mount_heathbeat():
	return bitarray('0')

