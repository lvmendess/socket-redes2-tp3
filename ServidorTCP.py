from socket import *

dict_Products = {'cerveja': 400, 'salada': 220, 'baguete': 120, 'espaguete':240, 'pizza': 600,
				 'cafe': 300, 'bolinho de carangueijo': 550, 'bolo de chocolate': 400,
				 'biscoitos': 280, 'cafe da manhã completo': 700, 'bolo rosa': 960}

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('Servidor aguardando mensagens')

def greeting():
	product = "Bem vindo ao Stardrop Saloon" + "\n"
	for k, v in dict_Products.items():
		product += k + " - Preço:" + str(v) + " ouros" + "\n"
	return product

def negotiate(product_name, valor):
	tolerancia = 15 #porcentagem de tolerância de preço
	x=dict_Products.get(product_name)
	min_preco = x * (1 - tolerancia / 100)
	if min_preco <= valor <= x: #valor proposto deve ser maior ou igual ao preço mínimo tolerado mas não pode ultrapassar o valor original
		return 'proposta aceita'
	else:
		return 'proposta rejeitada'

while True:
	connectionSocket, addr = serverSocket.accept()
	command = connectionSocket.recv(1024).decode()
	if command == 'menu':
		reply = greeting()
		connectionSocket.send(reply.encode())

	produto = connectionSocket.recv(1024).decode()
	if produto in dict_Products.keys():
		reply = 'produto encontrado'
		connectionSocket.send(reply.encode())
	else:
		reply = 'produto não encontrado'
		connectionSocket.send(reply.encode())

	connectionSocket.close()
