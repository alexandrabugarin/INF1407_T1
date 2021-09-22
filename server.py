from sys import exit
from os import abort
from internet import *
from config import PORT, DEFAULT_PAGES, DELAY, LOCAL_STORAGE_PATH
from _thread import *
import time

def requestReceiver(con, cliente):

    data = con.recv(1024).decode("utf-8")
    status = ''
    body = ''    
    if not data:
        print('')
        con.close()
        abort()
        return
              
    request = data.splitlines()[0]
    method, path, protocol = request.split(' ')

    if method != 'GET':
        status = "501"
        message = "Not Implemented"
        body = ''
    else:
        try:  
            if path == '/' or path == '/index.html':
                body = openfile(LOCAL_STORAGE_PATH + DEFAULT_PAGES[0])
            elif path != None: 
                body = openfile(LOCAL_STORAGE_PATH + path[1:])
            else:
                raise FileNotFoundError

            status = "200"
            message = "OK"
        
        except FileNotFoundError: 
            body = openfile(LOCAL_STORAGE_PATH + DEFAULT_PAGES[1])
            status = "404"
            message = "File Not Found"

    # connection closed

    con.send(
        (f'HTTP/1.1 {status} {message}').encode("utf-8"))
    con.send('\n\n'.encode("utf-8"))
    time.sleep(DELAY)
    con.send(body)
    con.close()

    return

def openfile(path):
    f = open(path, "rb")
    body = f.read()
    f.close()
    return body 

def verifyConfig(): 
    if (isinstance(PORT,int) and isinstance(DEFAULT_PAGES,list) and isinstance(LOCAL_STORAGE_PATH,str) and isinstance(DELAY, int)):
        return True
    else: 
        return False

def main():
    if(not verifyConfig()):
        print("Arquivo de configuração não existe ou faltam variaveis")
        abort()

    hostAddress = getHostAddress(PORT)
    fd = criaSocket(hostAddress)
    fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    bindaSocket(fd, PORT)
    print("Sevidor pronto em", hostAddress)
    escuta(fd)
    try: 
        while True:
            con, cliente = conecta(fd)
            start_new_thread(requestReceiver, (con, cliente))
    except: 
        print("Falha na conexão") 
    return

if __name__ == '__main__': 
    main()