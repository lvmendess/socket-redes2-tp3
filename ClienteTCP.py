from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input('Digite "menu" para ver os produtos:') #mensagem inicial que solicita o menu
clientSocket.send(sentence.encode())
menu = clientSocket.recv(1024)
print ('Resposta do servidor:', menu.decode())

produto = input('Digite o código do produto que deseja negociar:')
clientSocket.send(produto.encode())
produto = clientSocket.recv(1024).decode()
print ('Resposta do servidor:', produto)

if("produto encontrado" in produto):
    op = input ('Opções: comprar(1), fazer oferta(2), desistir(3). Digite o número da opção desejada:')
    clientSocket.send(op.encode()) #envia opção para o servidor
    op = int(op)
    
    match op:
        case 1: #aceitou comprar
            response = clientSocket.recv(1024)
            print('Resposta do servidor:', response.decode())
        case 2: #negociar
            offers = 0 #contador de ofertas
            response = ''
            while(offers < 5): #máximo 5 ofertas
                offer = input('digite o valor que deseja pagar:')
                clientSocket.send(offer.encode())
                offers+=1 #aumenta o contador
                response = clientSocket.recv(1024).decode()
                print('Resposta do servidor:', response)
                if('proposta aceita' in response): #servidor aceitou a proposta
                    break;
                else: #servidor não aceitou a proposta e enviou contraproposta
                    ans = input('aceitar contraproposta (s/n)? ')
                    clientSocket.send(ans.encode())
                    if(ans == 's'):
                        reply = clientSocket.recv(1024).decode()
                        print('Resposta do servidor:', reply)
                        exit();
            
            if(offers>=5): #cliente fez 5 ofertas e nenhuma foi aceita
                print('limite de propostas atingido')
            else:
                answer = clientSocket.recv(1024)
                print('Resposta do servidor:', answer.decode())
        case _:
            response = clientSocket.recv(1024)
            print('Resposta do servidor:', response.decode())

clientSocket.close()
