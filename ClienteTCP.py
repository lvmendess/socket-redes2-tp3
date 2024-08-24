from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input('Digite "menu" para ver os produtos:')
clientSocket.send(sentence.encode())
menu = clientSocket.recv(1024)
print ('Resposta do servidor:', menu.decode())

produto = input('Digite o código do produto que deseja negociar:')
clientSocket.send(produto.encode())
produto = clientSocket.recv(1024).decode()
print ('Resposta do servidor:', produto)

if("produto encontrado" in produto):
    op = input ('Opções: comprar(1), fazer oferta(2), desistir(3). Digite o número da opção desejada:')
    clientSocket.send(op.encode())
    op = int(op)
    
    match op:
        case 1:
            response = clientSocket.recv(1024)
            print('Resposta do servidor:', response.decode())
        case 2:
            offers = 0
            response = ''
            while(offers < 5):
                offer = input('digite o valor que deseja pagar:')
                clientSocket.send(offer.encode())
                offers+=1
                response = clientSocket.recv(1024).decode()
                print('Resposta do servidor:', response)
                if('proposta aceita' in response):
                    break;
            
            if(offers>=5):
                print('limite de propostas atingido')
            else:
                answer = clientSocket.recv(1024)
                print('Resposta do servidor:', answer.decode())
        case _:
            response = clientSocket.recv(1024)
            print('Resposta do servidor:', response.decode())

clientSocket.close()
