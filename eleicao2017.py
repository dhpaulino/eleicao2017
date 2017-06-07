#!coding:utf-8

from bitarray import *
from threading import Timer
import socket
from datetime import datetime, timedelta

N_NODES=4
MSG_SIZE = 1 #numeros de bits
HEARTHBEAT_TIME = 2  #segundos
HEARTHBEAT_MAX_WAIT_TIME = 8 #segundos
NODES={0: ("200.17.202.6", 5313), #macalan
        1: ("200.17.202.28", 5313), #orval
        2: ("10.254.224.17" ,5313), #montaro
        3: ("10.254.224.21", 5313)} #xereta
        
#("10.254.223.62", 5313)} #h58


 #("10.254.223.63", 5313), #h59
#("10.254.223.44", 5313)} #h40
 
# ("10.254.223.48", 5313), #h44 
 #("10.254.223.49", 5313), #h45
#("10.254.223.52", 5313)} #h48
# ("200.17.202.28", 5313), #orval
# ("200.17.202.11", 5313), #mumm

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
            print "lol" 
        except socket.error, e:                    
            nurgbytes=0
         # se chegou msg urgente
        if nurgbytes:
            print "\n** RECEBI AVISO DE {1} QUE O NOVO LIDER EH {0} ".format(ord(msgurg),id)
            print "** VOU ATUALIZAR LIDER PARA {0} ".format(ord(msgurg))
            try:
               # troca líder                             
                node.leader = ord(msgurg)
                print "** LIDER AGORA EH {0}".format(ord(msgurg))

            except KeyError:
                pass
        # trata msg normal
        else:
            try:
                #mensagem regular, heartbeat
                msg = bitarray(MSG_SIZE)
                nbytes = other_node.socket.recv_into(msg)
                #VERIFICAR AQUI PARA FIM DE CONEXAO? SIM, pois o buffer ainda está cheio, e send() pode continuar mandando. Palhaçadas do socket.
                if nbytes == 0:
                    print "\n** DETECTEI MORTE DO NODE {0} ".format(id)
                    del node.nodes_alive[id]
                    print "** REMOVI NODE {0} DA MINHA LISTA ".format(id)                       
                    #print "{0}Nodo {1} morto{2} POR TÉRMINO DE PROCESSO".format(bcolors.FAIL, id, bcolors.ENDC)
                    elect_leader(node, id)
                    print_alives(node)


                if(is_hearthbeat(msg)):
                    other_node.last_heathbeat = datetime.now()
                    if not other_node.first_heathbeat:
                        other_node.first_heathbeat = 1

            #print "Recebido msg de {1}:{0}".format(msg, id)

            except socket.error, e:
                                        
                # remove nó da lista de  vivos e elege líder (se necessário)
                print "\n** DETECTEI MORTE DO NODE {0} ".format(id)
                del node.nodes_alive[id]
                print "** REMOVI NODE {0} DA MINHA LISTA ".format(id)
                elect_leader(node, id)
                print_alives(node)
                continue

        #se o other_node.last_heathbeat já foi inicializado
        if other_node.last_heathbeat :
            now = datetime.now()
                        #print other_node, other_node.last_heathbeat, now

            #se o ultimo hearthbeat foi enviado em um tempo > do que HEARTHBEAT_MAX_WAIT_TIME
            if other_node.last_heathbeat + timedelta(seconds=HEARTHBEAT_MAX_WAIT_TIME) < now:
                del node.nodes_alive[id]
                elect_leader(node,id)
                
                print "\n {0}Nodo {1} morto{2} POR TIMEOUT".format(bcolors.FAIL, id, bcolors.ENDC)
                #se é o primeiro heartbeat do último nó enviar, elege líder:                                 
                if other_node.first_heathbeat == 1:
                    for i, oth in node.nodes_alive.items():
                        if not oth.first_heathbeat: #ainda nao recebi hearthbeat de todos os outros
                            break

                    #PRIMEIRA ELEICAO DE LIDER
                    node.leader = min(min(list(node.nodes_alive.keys())),node.id) 
                    print "\n** RECEBI HEARTHBEAT DE TODOS\n** PRIMEIRA ELEICAO DE LIDER.\n** LIDER EH {0}".format(node.leader)
                    for i, oth in node.nodes_alive.items():                            
                        print "** MANDEI LIDER PARA ", i
                        nsend = oth.socket.send(chr(node.leader),socket.MSG_OOB)
                        #print " ######### ENVIADOS URG {0}".format(nsend)

                        oth.first_heathbeat = 2 #nao será mais utilizado
            


def print_alives(node):
        print "\n** NODES CONECTADOS A MIM: ", list(node.nodes_alive.keys())    
def mount_heathbeat():
    return bitarray('0')

def is_hearthbeat(msg):
    return not msg[0] #tipo==0(False)

def elect_leader(node,id):
        if not node.nodes_alive.items():
            node.leader = node.id
            print "\n** TODOS MORRERAM, RESTOU EU"
            print "** LIDER AGORA EH {0}".format(node.leader)
        if node.leader == id:
            print_alives(node)
            node.leader = min(min(list(node.nodes_alive.keys())),node.id) #necessario, pois nodes_alive nao conte o proprio node
            print "\n** ATUALIZEI LIDER = ", node.leader

            #Se eu percebi que mudou lider, aviso aos demais. Caso fui avisado, nao reenvio aos outros
            
            print "** VOU MANDAR AVISO DE QUE TEMOS UM NOVO LIDER {0}".format(node.leader)
            for i, oth in node.nodes_alive.items():
                if i != id:
                    print "** MANDEI NOVO LIDER PARA ", i
                    nsend = oth.socket.send(chr(node.leader),socket.MSG_OOB)
                    #print " ######### ENVIADOS URG {0}".format(nsend)

