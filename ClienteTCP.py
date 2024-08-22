from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Digite "menu" para ver os produtos:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ('Resposta do servidor:', modifiedSentence.decode())

sentence = input('Digite o nome do produto que deseja negociar:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ('Resposta do servidor:', modifiedSentence.decode())
clientSocket.close()
