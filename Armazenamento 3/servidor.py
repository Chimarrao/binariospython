import socket
from nt import listdir
import os

# IP e porta
HOST = "127.0.0.3"
PORTA = 12345

# Tamanho do buffer
BUFFER_SIZE = 1024

# Seta o IP e Porta que o servidor vai "ouvir"
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))

# Coloca o servidor para "ouvir"
servidor.listen()

print("Aguardando conexões", HOST, PORTA)

# Retorna os arquivos disponíveis do servidor
def arquivosDisponiveis():
    arquivos = os.listdir(os.getcwd())
    arquivosDisponiveis = ""

    for arquivo in arquivos:
        arquivosDisponiveis += arquivo + "&"
        
    return arquivosDisponiveis

while True:
    cliente, endereco = servidor.accept()
    print("Cliente conectado", endereco)
    
    # Envia a lista de arquivos para o cliente
    arquivos = arquivosDisponiveis()
    cliente.send(str(arquivos).encode("utf-8"))
    
    # Recebe dados do cliente
    linha = cliente.recv(BUFFER_SIZE)
    
    # Recebe o nome do arquivo
    nomeArquivo = linha.decode("utf-8")
    print("Nome do arquivo: ", nomeArquivo)
    if nomeArquivo == "":
        continue
    
    # Quando o arquivo tiver um nome válido, ele será criado
    novoArquivo = open(nomeArquivo.replace(".", "_") + ".dat", "wb")

    # Recebe o arquivo em sí, em bytes
    linha = cliente.recv(BUFFER_SIZE)
    while linha:
        novoArquivo.write(linha)
        linha = cliente.recv(BUFFER_SIZE)
    
    novoArquivo.close()
    print("Arquivo recebido")

cliente.close()