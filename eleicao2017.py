from bitarray import *
from threading import Timer
import socket
from datetime import datetime, timedelta

N_NODES=4
MSG_SIZE = 1 #numeros de bits
HEARTHBEAT_TIME = 5 #segundos
HEARTHBEAT_MAX_WAIT_TIME = 8 #segundos
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

#Cores para deixar a saida mais bonita
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#TODO: usar mesmo objeto timer sempre
def hearthbeat_sender(node):
	node.send_hearthbeat()
	t = Timer(HEARTHBEAT_TIME, hearthbeat_sender, [node])
	t.start()
def message_reciver(node):

	for id, other_node in node.nodes_alive.items():
		try:
			msg = bitarray(MSG_SIZE)
			other_node.socket.recv_into(msg)
			if(is_hearthbeat(msg)):
				other_node.last_heathbeat = datetime.now()

			print "Recebido msg de {1}:{0}".format(msg, id)
		except socket.error, e:
			pass
		if other_node.last_heathbeat :
			now = datetime.now()
			if other_node.last_heathbeat + timedelta(seconds=HEARTHBEAT_MAX_WAIT_TIME) < now:
				del node.nodes_alive[id]
				print "{0}Nodo {1} morto{2}".format(bcolors.FAIL, id, bcolors.ENDC)

def mount_heathbeat():
	return bitarray('0')
def is_hearthbeat(msg):
	return not msg[0] #tipo==0(False)


