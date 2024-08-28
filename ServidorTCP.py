from socket import *
import random

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

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('Servidor aguardando mensagens')

def greeting(): #Cumprimenta o cliente e imprime o menu de produtos
	product = "Bem vindo ao Stardrop Saloon" + "\n"
	for k, v in products.items():
		product += k + " - " + v[0] +" - Preço: " + str(v[1]) + " ouros" + "\n"
	return product

#Calcula o valor mínimo aceitável com base em uma tolerância definida
def negotiate(product_key, valor):
	valor = int(valor)
	tolerancia = 20 #porcentagem de tolerância de preço
	for k, v in products.items():
		if (k == product_key):
			x = v[1]
	min_preco = x * (1 - tolerancia / 100)
	min_preco = int(min_preco)
	if min_preco <= valor <= x: #valor proposto deve ser maior ou igual ao preço mínimo tolerado mas não pode ultrapassar o valor original
		return 'proposta aceita'
	else:
		suggested = random.randint(min_preco, x) #sugere um preço aleatório entre o valor mímino aceitável e valor original
		return 'proposta rejeitada. contraproposta: '+str(suggested)+' ouros'

while True:
	connectionSocket, addr = serverSocket.accept()
	command = connectionSocket.recv(1024).decode()
	if command == 'menu':
		reply = greeting()
		connectionSocket.send(reply.encode())

	produto = connectionSocket.recv(1024).decode()
	if produto in products.keys(): #verifica se o produto existe
		for k, v in products.items(): 
			if (k == produto):
				x = v[1] #recebe o valor do produto
		reply = 'produto encontrado. Preço inicial: '+str(x)+' ouros';
		connectionSocket.send(reply.encode())

		op = connectionSocket.recv(1024).decode()
		op = int(op) #recebe a opção escolhida pelo cliente

		match op:
			case 1: #cliente aceita comprar pelo preço inicial
				reply = 'compra realizada com sucesso. volte sempre!'
				connectionSocket.send(reply.encode())
			case 2: #cliente quer negociar
				offers = 0 #contador de ofertas
				response = ''
				while(offers<5 and 'aceita' not in response): #limita número de ofertas
					offer = connectionSocket.recv(1024).decode()
					response = negotiate(produto, offer) #invoca função de negociação
					offers +=1
					connectionSocket.send(response.encode()) #'proposta aceita' ou 'proposta rejeitada+contraproposta'
					if('rejeitada' in response):
						ans = connectionSocket.recv(1024).decode() #recebe resposta do cliente sobre a contraproposta
						if(ans == 's'):
							reply = 'compra realizada com sucesso. volte sempre!'
							connectionSocket.send(reply.encode())
							exit();
					
				if('proposta aceita' in response):
					reply = 'compra realizada com sucesso. volte sempre!'
					connectionSocket.send(reply.encode())
					connectionSocket.close()
			case _: #cliente desistiu da compra
				reply = 'volte sempre!'
				connectionSocket.send(reply.encode())
	else:
		reply = 'produto não encontrado'
		connectionSocket.send(reply.encode())

	connectionSocket.close()
