from socket import *

products = {
	'1': ('cerveja', 400),
	'2' : ('salada', 220),
	'3' : ('pão', 120),
	'4' : ('espaguete', 240),
	'5' : ('pizza', 600),
	'6' : ('café', 300),
	'7' : ('bolinho de carangueijo', 550),
	'8' : ('bolo de chocolate', 400),
	'9' : ('biscoitos', 280),
	'10' : ('cafe da manhã completo', 700),
	'11' : ('bolo rosa', 960)
}

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
	for k, v in products.items():
		product += k + " - " + v[0] +" - Preço: " + str(v[1]) + " ouros" + "\n"
	return product

def negotiate(product_key, valor):
	valor = int(valor)
	tolerancia = 20 #porcentagem de tolerância de preço
	for k, v in products.items():
		if (k == product_key):
			x = v[1]
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
	if produto in products.keys():
		for k, v in products.items():
			if (k == produto):
				x = v[1]
		reply = 'produto encontrado. Preço inicial: '+str(x)+' ouros';
		connectionSocket.send(reply.encode())

		op = connectionSocket.recv(1024).decode()
		op = int(op)

		match op:
			case 1:
				reply = 'compra realizada com sucesso. volte sempre!'
				connectionSocket.send(reply.encode())
			case 2:
				offers = 0
				response = ''
				while(offers<5 and 'aceita' not in response):
					offer = connectionSocket.recv(1024).decode()
					response = negotiate(produto, offer)
					offers +=1
					connectionSocket.send(response.encode())
					
				if('proposta aceita' in response):
					reply = 'compra realizada com sucesso. volte sempre!'
					connectionSocket.send(reply.encode())
					connectionSocket.close()
			case _:
				reply = 'volte sempre!'
				connectionSocket.send(reply.encode())
	else:
		reply = 'produto não encontrado'
		connectionSocket.send(reply.encode())

	connectionSocket.close()
