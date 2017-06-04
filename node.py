import socket
import eleicao2017

class Node(object):
	id=None
	ip=None
	port=None
	socket=None #if the node is in "nodes_alive" it's the client socket within that node, if not it's the server socket of the node itself
	time_last_heathbeat=None
	nodes_alive=None

	def __init__(self, id, ip, port):
		self.id = id
		self.ip = ip
		self.port = port
		self.nodes_alive={}

	def bind_socket(self):
		"""Cria o servidor TCP do nodo de acordo com ip e porta informado"""

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  		self.socket.bind((self.ip, self.port))

	def connect(self, id, ip_dest, port_dest):
		"""Conecta com o nodo informado e adiciona na lista de nodos vivos. Retorna o nodo criado"""
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			s.connect((ip_dest, port_dest))
		except socket.error:
			return None
		node = self.add_node_alive(id, ip_dest, port_dest, s)
		return node

	def add_node_alive(self, id, ip, port, socket):
		node = Node(id, ip, port)
		node.socket = socket
		self.nodes_alive[id] = node
		return node
	
	def send_data(self, node, message):
		"""envia dado para o nodo informado"""
		node.socket.send(message)



