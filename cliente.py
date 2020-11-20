import os
import time
import socket
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import threading

# IP e porta
HOSTS = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
PORTA = 12345

# Tamanho do buffer
BUFFER_SIZE = 1024

# Quantidade de partes arquivo
ARQUIVO_PARTES = 4

# Abre a janela para escolher o arquivo
def menuArquivo():
    Tk().withdraw()
    pathArquivo = askopenfilename()
    pathArquivo = pathArquivo
    
    return pathArquivo

# Envia o arquivo
def enviaArquivo():
    pathArquivo = menuArquivo()

    # Abre o arquivo de fato
    arquivoRecebido = open(pathArquivo, "rb")

    # Testa o tamanho do arquivo
    tamanhoArquivo = os.path.getsize(pathArquivo)
    if round(tamanhoArquivo / (1024 * 1024), 3) > 4:
        print("\n" + "O arquivo não pode ser maior de 4mb !!" + "\n")
        input("Tecle enter para continuar....")
        return

    bufferLido = 0
    for host in HOSTS:
        # Conecta com o servidor
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.connect((host, PORTA))
        
        # Limpa o buffer do servidor
        servidor.recv(BUFFER_SIZE)
        
        # Envia o nome do arquivo e extensão
        servidor.send(pathArquivo.split("/")[-1].encode("utf-8"))
        time.sleep(0.1)

        # Envia o arquivo
        linha = arquivoRecebido.read(BUFFER_SIZE)
        print("Enviando arquivo ....")
        while linha:
            if bufferLido + 1024 > tamanhoArquivo / ARQUIVO_PARTES:
                break

            servidor.send(linha)
            linha = arquivoRecebido.read(BUFFER_SIZE)
            bufferLido += 1024

        bufferLido = 0

    arquivoRecebido.close()
    print("Enviado !")
    servidor.close()
    input("Tecle enter para continuar....")

# Trata os nomes de arquivos recebidos pelo servidor
def tratarArquivos(arquivos):
    # Remove o .dat
    arquivos = arquivos.replace(".dat", "")
    
    # Remove o auxiliar de formato
    arquivos = arquivos.replace("_", ".")

    # Remove o &, que divide arquivos
    arquivos = arquivos.replace("&", ",")

    # Remove o arquivo de servidor
    arquivos = arquivos.replace(",servidor.py", "")
    arquivos = arquivos.replace("servidor.py,", "")
    arquivos = arquivos.replace("servidor.py", "")
    
    # Remove a última vírgula
    arquivos = arquivos[:-1]
    
    return arquivos
    
# Lista os arquivos de todos os servidores
def listaArquivos():
    listaArquivos = {}
    for host in HOSTS:
        # Conecta com o servidor
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.connect((host, PORTA))
    
        # Adiciona os arquivos do servidor no dicionário
        listaArquivos[host] = servidor.recv(BUFFER_SIZE).decode("utf-8")
    
    print("Lista de arquivos:")

    # Printa os arquivos em tela, separados por servidor
    for host in listaArquivos:
        arquivos = listaArquivos[host]
        arquivos = tratarArquivos(arquivos)
        print("Servidor:", host, "->", arquivos)

    input("Tecle enter para continuar....")

opcao = ""
while opcao != "0":
    texto = "Escolha uma das opções a seguir" + "\n"
    texto += "1)Enviar arquivo" + "\n"
    texto += "2)Listar arquivos" + "\n"
    texto += "0)Sair" + "\n"
    opcao = input(texto)
    
    if opcao == "1":
        enviaArquivo()
    elif opcao == "2":
        listaArquivos()
        
    # Limpa o console
    os.system("cls")