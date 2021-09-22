from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, AI_ADDRCONFIG, AI_PASSIVE
from socket import IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR

def getHostAddress(porta):
    try: 
        hostAdress = getaddrinfo(None, porta, family = AF_INET, 
        type = SOCK_STREAM, proto = IPPROTO_TCP, flags = AI_ADDRCONFIG | AI_PASSIVE)
    except:
        print("Não obtive informações sobre o servidor", file=stderr)
        abort()
    return hostAdress

def criaSocket(enderecoServidor):
    fd = socket(enderecoServidor[0][0], enderecoServidor[0][1])
    if not fd: 
        print("Não consegui criar o socket", file=stderr)
        abort()
    return fd

def bindaSocket(fd, porta): 
    try: 
        fd.bind(('', porta))
    except: 
        print("Erro ao dar bind no socket do servidor", porta, file=stderr)
        abort()
    return

def escuta(fd): 
    try: 
        fd.listen(0)
    except: 
        print("Erro ao começar a escutar a porta", file=stderr)
        abort()
    print("Iniciando o serviço")
    return

def conecta(fd):
    (con, cliente) = fd.accept()
    print("Servidor conectado com", cliente)
    return con, cliente

