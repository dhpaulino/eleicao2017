#!coding:utf-8

from bitarray import *
from threading import Timer
import socket
from datetime import datetime, timedelta

N_NODES=3
MSG_SIZE = 1 #numeros de bits
HEARTHBEAT_TIME = 5 #segundos
HEARTHBEAT_MAX_WAIT_TIME = 8 #segundos
NODES={0: ("200.17.202.6", 5313), #macalan
 1: ("200.17.202.28", 5313), #orval
 2: ("10.254.223.52", 5313)} #h48

# 1: ("200.17.202.11", 5313), #mumm

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
                    #mensagem urgente, avisando que caiu aguém
                        msgurg = bytearray(1)
                        nurgbytes = other_node.socket.recv_into(msgurg,1,socket.MSG_OOB)
                                                                
		except socket.error, e:                    
                        nurgbytes=0
			pass

                if nurgbytes:
                        print "RECEBI AVISO DE QUE NODE {0} QUEBROU, FECHANDO CONEXAO".format(ord(msgurg))
                        del node.nodes_alive[ord(msgurg)] #????
                        elect_leader(node, ord(msgurg))
                        
    

                else:
                    try:
                 #mensagem regular, heartbeat
		        msg = bitarray(MSG_SIZE)
			nbytes = other_node.socket.recv_into(msg)
                        print "NBYTES=   ",nbytes
                        #VERIFICAR AQUI PARA FIM DE CONEXAO? SIM, pois o buffer ainda está cheio, e send() pode continuar mandando. Palhaçadas do socket.
                        if nbytes == 0:
                            del node.nodes_alive[id]
                            print "{0}Nodo {1} morto{2} POR TÉRMINO DE PROCESSO".format(bcolors.FAIL, id, bcolors.ENDC)
                            #to do: enviar menssagem de urgenca aos demais
                            elect_leader(node, id)



			if(is_hearthbeat(msg)):
				other_node.last_heathbeat = datetime.now()

			print "Recebido msg de {1}:{0}".format(msg, id)

                    except socket.error, e:
                        print "VOU MANDAR AVISE DE QUE {0} QUEBROU".format(id)
                        for i, oth in node.nodes_alive.items():
                            if id != i:
                                print "MANDEI PARA ", i
                                oth.socket.send(chr(id),socket.MSG_OOB)
                        pass

		#se o other_node.last_heathbeat já foi inicializado
		if other_node.last_heathbeat :
			now = datetime.now()
                        #print other_node, other_node.last_heathbeat, now

			#se o ultimo hearthbeat foi enviado em um tempo > do que HEARTHBEAT_MAX_WAIT_TIME
			if other_node.last_heathbeat + timedelta(seconds=HEARTHBEAT_MAX_WAIT_TIME) < now:
				del node.nodes_alive[id]
				print "{0}Nodo {1} morto{2} POR TIMEOUT".format(bcolors.FAIL, id, bcolors.ENDC)

def mount_heathbeat():
	return bitarray('0')

def is_hearthbeat(msg):
	return not msg[0] #tipo==0(False)

def elect_leader(node,id):
        if node.leader == id:
            node.leader = min(min(node.nodes_alive.values()).id,node.id) #necessario, pois nodes_alive nao conte o proprio node

            
